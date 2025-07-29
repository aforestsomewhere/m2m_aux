import glob

#This script firstly recurses through each PGDB folder, concatenating the compound-links.dat files into total_compounds.dat
#Usage: python compound_compendium.py

# Use a set to track seen lines and preserve order
seen = set()
unique_lines = []

# Loop over all compound-links.dat files two directories deep
for filepath in glob.glob('*/*/*/compound-links.dat'):
    with open(filepath, 'r') as infile:
        for line in infile:
            if line.lstrip().startswith('#'):
                continue  # Skip comment lines
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

# Write all unique, non-comment lines to the output file
with open('total_compounds.dat', 'w') as outfile:
    outfile.writelines(unique_lines)
