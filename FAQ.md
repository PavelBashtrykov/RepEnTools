# RepEnTools - FAQ

### Workflow

**Do I need to reinstall all the files for RepEnTools every time I run an analysis?**  
No, just once is enough. If you wish to change RepEnTools' reference directory for the files see Troubleshooting in README.  

---------------------------------------------------------
### Input data

**Can I use RepEnTools to analyse my noisy ChIP-seq dataset?**  
Yes, you can. Since RepEnTools leverages genome-wide alignments on REs for ChIP-seq and compares that to Input chromatin, it is possible to detect enrichments even with noisy datasets. Nevertheless, if the starting data are suboptimal the output is perforce going to be suboptimal, even if it is difficult to measure this directly in your data. 

**Can I use FASTQ data from CIDOP-seq, MBD-seq, or other experiments that are not ChIP-seq for analysis?**  
Yes, you can. As long as the data do not require additional processing steps, e.g. to remove extra barcodes or overlap with MNase peaks, RepEnTools can analyse your data. Scientifically sound judgement is of course necessary.

**Can I use single-end (SE) FASTQ data for analysis?**  
At the moment that is not possible. You would have to modify the code, download the correct adapter file and modify the settings in Trimmomatic and in HISAT2. The Galaxy workflow (usegalaxy.eu/u/choudalakis_m/w/repentools-part1-single-end-fastqhisat2optchm13bwgprim) can guide you. Keep in mind that in our tests, SE mapping leads to ~10% lower alignment efficiency than PE mapping, using the same data. So, check the quality control (QC) data carefully, especially to verify adequate mapping.

**Can I use very noisy, single-end, 36 bp FASTQ data with only 100,000 reads for analysis?**  
Yes, you can. That doesn’t mean you should. RepEnTools cannot fix suboptimal data. 

---------------------------------------------------------
### Other organisms

**Can I use RepEnTools to analyse mouse data?**  
If you have a suitable annotation file, you could try that. At the moment of writing (Oct. 2023), no T2T mouse genome has been published, and many repetitive parts of the genome are not covered. Also, because of the nature of rodent REs, we advise caution in interpreting such data. Finally, diligent QC is necessary given the known challenges in mouse ChIP-seq experiments. 

**I have made the annotation files to use RepEnTools with data from other organisms. How can I share this with the community?**  
We would be delighted to hear from you on github! We aim for RepEnTools to be an evolving collection of tools, with community participation and corresponding attribution of credit.

---------------------------------------------------------
### REs & RepEnTools

**Where can I find more information on RepEnTools and the data used to validate it for chm13v2?**  
Our publication is available here (LINK).

**Why do you remove certain superfamilies of repeat elements in the final report?**  
As shown in our publication, out of > 14340 Simple repeats some (< 500) are less reliably handled than all other REs. Many have low genome-wide abundance, meaning they need deeper than usual sequencing to have a reliable probability of detection. Unknown, low complexity REs and tRNA genes exhibit a similar trend. Simple repeats, low complexity, snRNA, and some other RE (super)families might not be fully annotated in a genome, due to practical limitations from repeat masker (https://repeatmasker.org/webrepeatmaskerhelp.html). In an abundance of caution, we recommend great care in interpreting these results.  

**Is there something else I should be mindful of when interpreting results from RepEnTools?**  
Yes! Possibly the two least obvious and yet important points are that  

•	the criteria for classification of individual REs into specific subfamilies etc might not be necessarily compatible with ChIP-seq and RepEnTools analyses. A good example are human L1PAs. In full-length they are ~ 7 kb long, and they have been classified based on the divergence of the 3' end. However, the 5' ends have different (slower) divergence rates. As do the coding regions. Moreover, repeat masker uses HMM profiles that describe each of the three parts separately and then compiles that information to annotate L1PA instances in the reference genome (see repeatmasker.org/webrepeatmaskerhelp). In our publication, we verified that L1PAs and SVAs are very reliably recovered (> 97%) using simulated data. 

•	nomenclature of REs can be extremely inconsistent, hindering even simple literature research (e.g. LTR22, LTR22A, and LTR22B are collectively named HERVK22I or HERV-K(HML-5) or NMWV2).

**Are there other considerations when using RepEnTools?**  
Yes, some. You can read them in Considerations.md.

**Where can I find more information on repeat elements and computational analyses thereof?**  
Our publication cites a number of great works. 
Also, we regularly consult the following online resources:
- dfam RE database (https://dfam.org)  
- TE hub (https://TEhub.org)

A very good overview of computational methods and their characteristics can be gained by reading Goerner-Potvin P, Bourque G. Computational tools to unmask transposable elements. Nat Rev Genet. 2018 (https://pubmed.ncbi.nlm.nih.gov/30232369/).

**Which is the coolest and best RE?**  
The one and only Колобок!  

<img title="Kolobok" style="float:right;margin:00px 400 0 0px" id="Kolobok" src="images/RepEnTools_Колобок-малый.png" >  