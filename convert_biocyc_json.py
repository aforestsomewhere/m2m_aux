import json
import argparse
import os
import pandas as pd

#This script takes M2M output files (.json)
#It will strip and clean the Biocyc IDs,
#then lookup the compound_compendium file to replace them with 'informative' names.

#Usage: python convert_biocyc_json.py input.json compund_compendium.dat --output output.json

#function to clean biocyc IDs
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

# Recursive function to traverse and update JSON
def transform_json(data, lookup_dict):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = replace_if_biocyc(key, lookup_dict)
            new_data[new_key] = transform_json(value, lookup_dict)
        return new_data
    elif isinstance(data, list):
        return [transform_json(item, lookup_dict) for item in data]
    elif isinstance(data, str):
        return replace_if_biocyc(data, lookup_dict)
    else:
        return data

#function to swap Biocyc IDs with synonyms from lookup table
def replace_if_biocyc(value, lookup_dict):
    if isinstance(value, str) and value.startswith("M_"):
        cleaned = parse_biocyc_id(value)
        return lookup_dict.get(cleaned, cleaned)
    return value

#Parse command-line arguments
parser = argparse.ArgumentParser(description='Convert Biocyc IDs in JSON file using lookup table.')
parser.add_argument('json_file', help='Path to the JSON input file')
parser.add_argument('lookup_table', help='Path to the compound_compendium lookup table file (*.dat)')
parser.add_argument('--output', help='Output JSON file name (default: updated_<input>.json)', default=None)

args = parser.parse_args()

# Load lookup table
try:
    df = pd.read_csv(args.lookup_table, sep="\t", header=None, usecols=[0, 3])
    lookup_dict = dict(zip(df[0].astype(str), df[3].astype(str)))
except Exception as e:
    print(f"Failed to load lookup table: {e}")
    exit(1)

# Load and transform JSON
try:
    with open(args.json_file, "r") as f:
        data = json.load(f)
except Exception as e:
    print(f"Failed to load JSON: {e}")
    exit(1)

updated = transform_json(data, lookup_dict)

# Output
output_file = args.output or f"updated_{os.path.basename(args.json_file)}"
with open(output_file, "w") as f:
    json.dump(updated, f, indent=4)

print(f"Updated JSON written to {output_file}")

