#!/usr/bin/env python

################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

import argparse
import pandas as pd
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--report", help="RepEnTools report file", type=str, required=True)

parser.add_argument("-v", help="Volcano plot file name", type=str, required=False)
parser.add_argument("-f", help="Families statistics file name", type=str, required=False)
parser.add_argument("-b", help="Bar plot file name", type=str, required=False)

args = parser.parse_args()

VOLCANO_PLOT = "ret_volcano_plot.jpg"
FAMILIES_SUMMARY = "ret_report_families.csv"
BAR_PLOT = "ret_top_hits.jpg"

if args.v:
    VOLCANO_PLOT = args.v
if args.f:
    FAMILIES_SUMMARY = args.f
if args.b:
    BAR_PLOT = args.b


#read RepEnTools results file
df = pd.read_csv(args.report, sep=";")

# horisontal line
horisontal_line = df.loc[df["p-adj"] > 0.05].iloc[0]["log10(p-value)"]

rcParams.update({'figure.autolayout': True})
fig, ax = plt.subplots(figsize=(9,5))
sns.set_theme(style="ticks", palette="deep", color_codes=True)
sns.scatterplot(data=df, x="log2(FC)", y="log10(p-value)", edgecolors=None, alpha=1, s=20, legend=False, color=df["color"])
ax.set(xlabel="log2(FC)")
ax.set(ylabel="-log10(p-value)")
ax.axhline(horisontal_line, ls='--', c='grey')
ax.axvline(0.5, ls='--', c='grey')
ax.axvline(-0.5, ls='--', c='grey')
plt.tight_layout()
fig.savefig(VOLCANO_PLOT,dpi=300)
plt.clf()

# group by families
summary = df.groupby("Group").count().Geneid.to_frame()
summary.rename(columns={"Geneid":"Counts"}, inplace=True)
summary["Sum_En_Rep1"] = df.groupby("Group").sum().Rep1_enriched
summary["Sum_En_Rep2"] = df.groupby("Group").sum().Rep2_enriched
summary["nor_sum_en_rep1"] = summary["Sum_En_Rep1"] / summary["Counts"]
summary["nor_sum_en_rep2"] = summary["Sum_En_Rep2"] / summary["Counts"]
summary["mean"] = summary[['nor_sum_en_rep1', 'nor_sum_en_rep2']].mean(axis=1)
summary["SD"] = summary[['nor_sum_en_rep1', 'nor_sum_en_rep2']].std(axis=1,ddof=0)
summary["RSD%"] = summary["SD"] / summary["mean"]*100
summary["ABS(z)"] = ((summary["mean"] - 1) / summary["SD"]).abs()
summary["p-value"] = 1 - norm.cdf(summary["ABS(z)"])
summary = summary.sort_values(by='mean', ascending=False)
summary = summary.reset_index()
summary.to_csv(FAMILIES_SUMMARY, sep=";", index=False)

# select enriched groups
top = summary.loc[(summary['p-value'] <= 0.05) & (summary["mean"] >= 0)].iloc[:10]
first = top.loc[:, ("Group", "nor_sum_en_rep1")]
first.rename(columns={'nor_sum_en_rep1':'enrichment'}, inplace=True)
second = top.loc[:, ("Group", "nor_sum_en_rep2")]
second.rename(columns={'nor_sum_en_rep2':'enrichment'}, inplace=True)
top_plotting = pd.concat([first, second])

rcParams.update({'figure.autolayout': True})
fig, ax = plt.subplots(figsize=(9,5))
sns.set_theme(style="ticks", palette="deep", color_codes=True)
sns.barplot(ax=ax,data=top_plotting, x="enrichment", y="Group", zorder=5, errorbar="sd", capsize=.15, lw=1)
sns.barplot(ax=ax,data=top_plotting, x="enrichment", y="Group", zorder=10, color="yellowgreen", errorbar=None)
ax.set(xlabel="ChIP/Input")
ax.set(ylabel=None)
plt.tight_layout()
fig.savefig(BAR_PLOT,dpi=300)
