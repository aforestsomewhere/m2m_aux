import os
import pandas as pd

# Read the TSV file with a different encoding
taxon_df = pd.read_csv('taxon_id.tsv', sep='\t', encoding='ISO-8859-1')

# Create a dictionary from the TSV file
taxon_dict = dict(zip(taxon_df['species'], taxon_df['taxon_id']))

# Root directory to start the search (current working directory)
root_directory = os.getcwd()

# Iterate over all files in the directory tree
for root, dirs, files in os.walk(root_directory):
    for file_name in files:
        # Change to .gbff here if bakta output
        if file_name.endswith('.gbk'):
            # Extract the species name from the directory name
            species_name = os.path.basename(root)
            if species_name in taxon_dict:
                taxon_id = taxon_dict[species_name]

                # Full path to the .genbank file
                file_path = os.path.join(root, file_name)
                
                # Read the file content
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                # Flag to check if db_xref is already present
                dbxref_present = False
                
                # Write the modified content back to the file
                with open(file_path, 'w') as file:
                    in_source_section = False
                    for line in lines:
                        if line.strip().startswith("FEATURES"):
                            in_source_section = False
                        if line.strip().startswith("source"):
                            in_source_section = True
                        if in_source_section and '/db_xref="taxon:' in line:
                            dbxref_present = True
                        file.write(line)
                        if in_source_section and line.strip() == '/mol_type="genomic DNA"' and not dbxref_present:
                            file.write(f"                     /db_xref=\"taxon:{taxon_id}\"\n")
                            in_source_section = False  # Ensure we don't add multiple times

                print(f"Processed {file_path}, db_xref present: {dbxref_present}")

print("All files have been processed.")
