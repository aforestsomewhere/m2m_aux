#!/bin/bash

# Convert any .gbff files to .gbk for standardisation
for file in *.gbff; do
  filename="${file%.gbff}"
  python convert_gbff_gbk.py "$filename".gbff "$filename".gbk
done

#Remove any remaining .gbff files
rm -rf *.gbff

# Loop through each .gbk file in the current directory
for file in *.gbk; do
  # Remove the .gbk suffix from the filename to get the directory name
  dirname="${file%.gbk}"
  # Create the directory
  mkdir -p "$dirname"
  
  # Optionally, move or symlink the file into the newly created directory
  #cp "$file" "$dirname"
  #ln -s "$dirname"/"$dirname".gbff "$dirname".gbff
  mv "$dirname".gbk "$dirname"/
done

#Add db_xref taxon id information to .gbk files
python add_dbxref.py

#Clean up files
if [ -d ".git" ]; then
  echo "Removing .git directory..."
  rm -rf .git
  echo ".git directory removed."
else
  echo "No .git directory found."
fi
