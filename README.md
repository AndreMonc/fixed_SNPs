# fixed_SNPs.py: a program to identify fixed SNPs between parental species.

##### Written by Andre E. Moncrieff, 2021.

## Introduction 

This program is designed to filter a VCF file containing individuals of two parental species and hybrids between them. The goal is to then identify and select any SNPs that are homozygous and different 100% of the time in the parental species **AND** retain the hybrid genotypes at these sites. These data can then be used to test if hybrids are F1 hybrids (if all/most sites are heterozygous in hybrids) and the degree of backcrossing. Calculations of the interspecific heterozygosity from these data at fixed sites can also be used as input for triangle plots in  [INTROGRESS](http://www.uwyo.edu/buerkle/software/introgress/).

## Step-by-step instructions 
#### (*Sorry, a few quick manual steps*)

- Remove the header lines in your VCF before the line starting with '#CHROM'
- Change your vcf file extension to .txt
- You need to edit the .py script "parse_row" function to indicate what columns of the VCF contain parental1 and parental2 (using standard python list splicing). The first column with genotypes is column 0. Parental species do not *need* to be sorted in the VCF but it makes identifying the columns easier.
- Run: `python fixed_SNPs.py --vcf_file yourVCF.txt` 
- Output file is csv: 'fixed_snps_vcf.csv' for easy visualization
- Finally, if desired, add full VCF header info and change extension back to .vcf

## Citation

**Moncrieff, A.E.** 2021. Fixed_SNPs v1.0: a program to identify fixed SNPs between parental species.