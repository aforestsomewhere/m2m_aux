import sys
from Bio import SeqIO

#converts .gbff to .gbk for m2m

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Usage: python convert_gbff_gbk.py <input_file.gbff> <output_file.gbk>")
    sys.exit(1)

# Define the input and output file paths
input_file = sys.argv[1]
output_file = sys.argv[2]

# Read the input .gbff file and write to the .gbk file
with open(input_file, "r") as input_handle, open(output_file, "w") as output_handle:
    sequences = SeqIO.parse(input_handle, "genbank")
    SeqIO.write(sequences, output_handle, "genbank")

print(f"Converted {input_file} to {output_file}")
