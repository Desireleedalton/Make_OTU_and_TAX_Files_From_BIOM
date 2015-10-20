## i am a change

#!/usr/bin/python
# Graeme Fox - June 2015
# graeme.fox@manchester.ac.uk
# Takes a BIOM file from a database (Qiita for example)
# Converts it into separate OTU table and TAXA file
# Tested on (L)ubuntu 15.04 only.

import Bio, subprocess, csv, sys, re, argparse, os
from Bio import SeqIO

parser = argparse.ArgumentParser(description='none')
parser.add_argument('-i','--input1', help='Input_file', required=True)
args = vars(parser.parse_args())
input_file = args['input1'];

# Get the filename without file extension
match = re.search(r'.*\.', input_file)
if match:
    no_extension = match.group().rstrip('.')

# Get the columns and put out into appropriate file
with open (input_file) as csvfile:
    csv_f = csv.reader(csvfile, delimiter='\t')
# Skip the header line
    csv_f.next()
    first_row = next(csv_f)
    num_cols = len(first_row)

#####################
# Write the output files
#####################
# get the first and final columns and put into _tax file
    taxo_file = no_extension + '_tax.csv'
    otu_file = no_extension + '_OTU_counts.csv'
    header = "OTU_ID,Kingdom,Phyla,Class,Order,Family,Genus,Species"
    with open(taxo_file, 'w') as f, open(otu_file, 'w') as g:
# write header for each file
        f.write(header + "\n")
        for item in first_row[:-1]:
            g.write(item + ",")
        g.write("\n")
        for row in csv_f:
            # write the tax_file
            f.write(row[0] + ",")
            taxa_split = row[num_cols - 1].replace(";",",")
            f.write(taxa_split + "\n")
            # write the otu file
            n = 0
            while n < num_cols-1:
                g.write(row[n] + ",")
                n = n+1
            g.write("\n")
