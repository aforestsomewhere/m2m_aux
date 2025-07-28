import os
import pandas as pd
from biocyc import biocyc
from xml.etree import ElementTree as ET

def fetch_common_name(parsed_id):
    # Set the organism to MetaCyc
    biocyc.set_organism('meta')
    
    try:
        # Fetch the metabolite information
        metabolite = biocyc.get(parsed_id)
        
        # Check if the metabolite object has the attribute 'name' or 'synonyms'
        if hasattr(metabolite, 'name') and metabolite.name:
            return metabolite.name
        elif hasattr(metabolite, 'synonyms') and metabolite.synonyms:
            return metabolite.synonyms[0] if metabolite.synonyms else parsed_id
        else:
            print(f"Common name not found for {parsed_id}")
            return parsed_id
    except ET.ParseError as e:
        print(f"XML parsing error for {parsed_id}: {e}")
        return parsed_id
    except Exception as e:
        print(f"Error fetching common name for {parsed_id}: {e}")
        return parsed_id  # Fallback to the parsed ID if no common name is found

def parse_biocyc_id(biocyc_id):
    # Remove "M_" prefix
    biocyc_id = biocyc_id.lstrip("M_")
    
    # Replace "__45__" with "-"
    biocyc_id = biocyc_id.replace("__45__", "-")
    
    # Replace "__43__" with "+"
    biocyc_id = biocyc_id.replace("__43__", "+")
    
    # Remove "_c" suffix
    if biocyc_id.endswith("_c"):
        biocyc_id = biocyc_id[:-2]
    # Remove "_e" suffix
    if biocyc_id.endswith("_e"):
        biocyc_id = biocyc_id[:-2]
    
    return biocyc_id

def main():
    input_file = 'input.txt'
    mapping = {}

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        for biocyc_id in lines:
            biocyc_id = biocyc_id.strip()  # Remove any surrounding whitespace or newline characters
            parsed_id = parse_biocyc_id(biocyc_id)
            common_name = fetch_common_name(parsed_id)
            mapping[parsed_id] = common_name

        # Save the mapping to a CSV file
        df = pd.DataFrame(list(mapping.items()), columns=['biocyc_id', 'common_name'])
        df.to_csv('biocyc_to_common.csv', index=False)
        print("Mapping saved to biocyc_to_common.csv")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set your proxy if necessary
    os.environ['http_proxy'] = ''  # Replace with your proxy if needed
    main()
