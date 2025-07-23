Auxiliary scripts for M2M.

Prerequisites:

In working directory: 

1) Genbank (.gbff or .gbk files) for genomes to be used in M2M.
2) taxon_id.csv: 2 column, tab-separated file

| species  | taxon_id |
| ------------- | ------------- |
| strain_name_1  | 123  |
| strain_name_2  | 456  |

Note: Per https://github.com/AuReMe/metage2metabo/issues/56, NCBI taxon ID should be added to each .gbk file.

The scripts will standardise all extensions to .gbk, organise .gbks in respective input folders and insert NCBI tax ID's into each .gbk.
