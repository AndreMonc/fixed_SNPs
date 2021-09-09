# !/usr/bin/env python
# encoding: utf-8

"""
Identify fixed SNPs
Copyright 2021 Andre E. Moncrieff. All rights reserved.
"""

import argparse
import pandas
import numpy
import csv
import itertools
import re


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vcf_file", required=True,
                        help="Enter the file name (including .vcf extension)",
                        type=str)
    args = parser.parse_args()
    return args


def read_in_csv(txt_file_dataframe):
    raw_dataframe = pandas.read_csv(txt_file_dataframe,
                                    sep='\t',
                                    encoding = "ISO-8859-1",
                                    dtype=str)
    return raw_dataframe


def rows_to_list(vcf_df):
    list_of_rows = vcf_df.values.tolist()
    return list_of_rows


def trim_lists(list_of_rows):
    #takes out the first 9 columns of VCF: '#CHROM' through 'FORMAT'
    #The point is to get a dataframe of the individuals only
    trimmed_list_of_rows = []
    for item in list_of_rows:
        trimmed_row= item[9:]
        trimmed_list_of_rows.append(trimmed_row)
    return trimmed_list_of_rows


def genotype_list(list_of_rows):
    #take the genotypes only from the columns for each individual
    genotypes_by_row = []
    for row in list_of_rows:
        rowlist = []
        for item in row:
            genotype = item.split(':')[0]
            rowlist.append(genotype)
        genotypes_by_row.append(rowlist)
    return genotypes_by_row


def parserow(list_of_genotypes):   
    row_indicator = []
    for item in list_of_genotypes:
        #row_list = []
        #item.append(row_indicator)
        parental1a = item[0:9] #UPDATE as needed for your dataset
        parental2 = item[10:15] #UPDATE as needed for your dataset
        parental1b = item[15:24] #UPDATE as needed for your dataset
        parental1 = parental1a + parental1b #Notice, parental columns don't need to be adjacent
        parental1_set = set(parental1)
        parental2_set = set(parental2)
        homosetref = set(['0/0', '0|0'])
        homosetalt = set(['1/1', '1|1'])
        #templist =[]
        if parental1_set.issubset(homosetref) == True and parental2_set.issubset(homosetalt) == True:
            row_indicator.append("yes")
        elif parental1_set.issubset(homosetalt) == True and parental2_set.issubset(homosetref) == True:
            row_indicator.append("yes")
        else:
            row_indicator.append("no")
    return row_indicator


def add_column_pandas(vcf_df, indicator_row):
    vcf_df['Indicator'] = indicator_row
    return vcf_df


def filter_dataframe(new_vcf_df):
    filtered_dataf = new_vcf_df[new_vcf_df['Indicator'].isin(['yes'])]
    return filtered_dataf


def delete_column(filtered_dataf):
    del filtered_dataf['Indicator']
    return filtered_dataf


def main():
    #create args object
    args = parser()
    #read in dataframes
    vcf_df = read_in_csv(args.vcf_file)
    #print(vcf_df)
    list_of_rows = rows_to_list(vcf_df)
    #print(list_of_rows)
    trimmed_list_of_rows = trim_lists(list_of_rows)
    #print(trimmed_list_of_rows)
    list_of_genotypes = genotype_list(trimmed_list_of_rows)
    #print(list_of_genotypes)
    row_indicator = parserow(list_of_genotypes)
    #print(row_indicator)
    df_with_indicator_column = add_column_pandas(vcf_df, row_indicator)
    filtered_df = filter_dataframe(df_with_indicator_column)
    final_fixed_SNPs_df = delete_column(filtered_df)
    #print(final_fixed_SNPs_df)
    final_fixed_SNPs_df.to_csv('fixed_snps_vcf.csv', sep='\t', index=False)

'''
    with open('genotypes.txt', 'w') as f:
        for item in list_of_genotypes:
            f.write("%s\n" % item)
'''

if __name__ == '__main__':
    main()