#!/usr/bin/env python

################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

import os
import argparse
import pandas as pd
import numpy as np
from scipy.stats import norm

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--report", help="featureCounts report file", type=str, required=True)
parser.add_argument("-s", "--summary", help="featureCounts summary file", type=str, required=True)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-g", "--get", help="Search flagstat files in a current working directory", action="store_true")
group.add_argument("-f", "--flagstat", help='Provide a quoted space separated list of flagstat report files: "file1 file2 file3"', type=str)

parser.add_argument("-c", help="Complete report file name", type=str, required=False)
parser.add_argument("-t", help="Filtered report file name", type=str, required=False)
parser.add_argument("-e", help="Experiment summary file name", type=str, required=False)
args = parser.parse_args()

FULL_REPORT_NAME = "ret_report.csv"
FILTERED_REPORT_NAME = "ret_report_ChIP.csv"
SUMMARY_NAME = "ret_experiment_summary.csv"

if args.c:
    FULL_REPORT_NAME = args.c
if args.t:
    FILTERED_REPORT_NAME = args.t
if args.e:
    SUMMARY_NAME = args.e

#read featureCounts file
df = pd.read_csv(args.report, sep="\t", skiprows=[0])

# make column "Group"
df = df.rename(columns={"transcript_id": "Group"})
df.loc[df["Group"].str.endswith("L)"), "Group"] = "ahor" # rename active hor elements
df["Group"] = df["Group"].apply(lambda x: x.split("_")[0])

# get samples names
chips = [x for x in df.columns if "ChIP" in x]
inputs = [x for x in df.columns if "input" in x]
samples = [x.rstrip("_ChIP.bam") for x in chips]

# in Inputs replace 0 values by 0.1
zero_replacement = 0.1
for x in inputs+chips:
    df.replace({x: {0:zero_replacement}}, inplace=True)

# read flagstat files from directory
if args.get:
    flagstatfiles = [f for f in os.listdir('.') if os.path.isfile(f) and "flagstat" in f]
elif args.flagstat:
    flagstatfiles = [x for x in args.flagstat.split(" ")]

# normalise by primary mapped reads
for flagstat in flagstatfiles:
    name = flagstat.split("_flagstat.txt")[0]
    if name not in df.columns.str.strip(".bam"):
        continue
    flagstat_df = pd.read_csv(flagstat)
    primary_mapped = int(flagstat_df.iloc[6,0].split(" ")[0])
    df[name+"_norm"] = df[name+".bam"] / primary_mapped

# compute Enrichment: n.Chip
enriched = []
for x in samples:
    df[x+"_enriched"] = df[x+"_ChIP_norm"] / df[x+"_input_norm"]
    enriched.append(x+"_enriched")

# Compute average of two repeats
df["Average"] = df[enriched].mean(axis=1)

# Compute SD of two repeats
df["SD"] = df[enriched].std(axis=1, ddof=0)

# z score
df["z-score"] = (df["Average"] - 1) / df["SD"]
df.loc[np.isinf(df["z-score"]), "z-score"] = 0  # if SD=0, leads to inf/-inf result, this converts it to 0
df["z-score"] = df["z-score"].abs()

# p value
df["p-value"] = 1 - norm.cdf(df["z-score"])
df.loc[df["p-value"] < 10**(-16), "p-value"] = 10**(-16) # trim at 10e-16
df["log10(p-value)"] = - np.log10(df["p-value"])
df = df.sort_values(by='p-value', ascending=True)
n_elements = df.shape[0]
df["rank"] = [x for x in range (1, n_elements+1)]
df["p-adj"] = df["p-value"] * n_elements / df["rank"]
df["log2(FC)"] = np.log2(df["Average"])

# colors for volcano plot
depleted = "salmon"
enriched = "yellowgreen"
not_significant = "grey"

conditions = [
    (df['log2(FC)'] <= -0.5) & (df["p-adj"] <= 0.05),
    (df['log2(FC)'] >= 0.5) & (df["p-adj"] <= 0.05)
]

choices = [depleted,enriched]
df['color'] = np.select(conditions, choices, default=not_significant)


# save a report file
cols = ["Chr", "Start", "End", "Strand"]
df = df.drop(columns=cols)
df.to_csv(FULL_REPORT_NAME, sep=";", index=False)

# generate a second file w/o Simple_repeat, Low_complexity, tRNA, Unknown
tags = ["Simple", "Low", "tRNA", "Unknown"]
df = df[~df.Group.str.contains('|'.join(tags), regex=True)]
df.to_csv(FILTERED_REPORT_NAME, sep=";", index=False)

# Generate an experiment summary table
fcs = pd.read_csv(args.summary, sep="\t")
headers = ["Rep1_ChIP", "Rep2_ChIP", "Rep1_input", "Rep2_input", "Rep1_ChIP/input", "Rep2_ChIP/input"]
values = []
for header in headers[:4]:
    flagstat_df = pd.read_csv(header + "_flagstat.txt", sep="+", engine='python')
    ratio = fcs.iloc[0][header + ".bam"] / flagstat_df.iloc[6,0]
    values.append(ratio)

values.append(values[0]/values[2])
values.append(values[1]/values[3])

with open(SUMMARY_NAME, "w") as f:
    f.write(";".join(headers))
    f.write("\n")
    f.write(";".join([str(s) for s in values]))