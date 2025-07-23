#!/bin/bash

# Loop through each .gbk file in the current directory
for file in *.gbk; do
  # Remove the .gbff suffix from the filename to get the directory name
  dirname="${file%.gbk}"
  
  # Create the directory
  mkdir -p "$dirname"
  
  # Optionally, move or symlink the file into the newly created directory
  #cp "$file" "$dirname"
  #ln -s "$dirname"/"$dirname".gbff "$dirname".gbff
  mv *"$dirname"* "$dirname"
done
