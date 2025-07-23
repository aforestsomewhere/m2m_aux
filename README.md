Auxiliary scripts for M2M.

Prerequisites:

In working directory: 

1) Genbank (.gbff or .gbk files) for genomes to be used in M2M.
2) taxon_id.tsv: 2 column, tab-separated file
3) Active environment with Python modules sys, Bio, pandas, os (if on Migale: 'conda activate metage2metabo-1.6.1' is sufficient.

| species  | taxon_id |
| ------------- | ------------- |
| strain_1  | 1597  |
| strain_2  | 146474  |

Note: Per https://github.com/AuReMe/metage2metabo/issues/56, NCBI taxon ID should be added to each .gbk file.

The scripts will standardise all extensions to .gbk, organise .gbks in respective input folders and insert NCBI tax ID's into each .gbk.

