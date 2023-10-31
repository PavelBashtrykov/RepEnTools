# Considerations regarding the use of RepEnTools

### At the moment, RepEnTools cannot:    
•	Analyse all Simple repeats precisely. To be more specific, a subset of <700 Simple repeats of the 14,346 Simple repeats, as well as a small number of tRNAs genes, Unknown and Low complexity REs are consistently sub-optimally reproduced in RepEnTools analyses. In an abundance of caution, we recommend great care in interpreting these results.

•	Find sharp enrichments in very large REs with a lot of Input signal (e.g. α-Satellites). RepEnTools analyse the sum of ChIP-seq reads on a RE and compare that to Input. Therefore, sharp enrichments in ChIP on one portion of the RE versus broad Input signal over the entirety of a megabase long RE will evidently not result in robust enrichment. At the moment, this is a limitation without an available solution. 

•	Identify novel repetitive sequences, insertions or deletions. We selected the most advantageous approach, for high efficiency and low computational cost, using the RMSK annotation and thus using previously annotated REs.  Alternatives have their own strengths but also drawbacks, see Goerner-Potvin P and Bourque G, 2018 (https://pubmed.ncbi.nlm.nih.gov/30232369/).

•	Analyse data from organisms other than human. If a complete (T2T) genome with repeat masker (RMSK) annotation is available, it is possible to develop this. Adjusting the reference file is unfortunately non-trivial, and validation is highly recommended. In our experience, the minimum control is to verify the reproducible assignment using simulated sequencing data with adequate depth, e.g. using ART. 

### Technical considerations  
•	As we demonstrated in our publication, low sequencing depth in ChIP or Input samples will adversely impact any RE analysis. This was evidenced by the non-linear improvement of RE coverage with increasing genome-wide coverage.

•	Although not addressed in our publication, we also saw that single-end (SE) analysis results in ~10% lower alignment efficiency than PE mapping, using the same data. Also, the advantages of 150 bp in RE analysis are evident and well-known.

### Computational considerations    
•	It is best to use T2T genomes, as these represent the entire genomic sampling space. This is a minimum requirement to give REs approximately correct statistical distribution. Samples from different individuals and especially from diseases & treatments that affect genomic stability, diverge from what is found in reference assemblies. Moderate sequence evolution should be manageable by HISAT2 – a de Bruijn mapper – and the use of Input chromatin data normalises for moderate changes in RE distributions, whether due to genomic material source or experimental and computational process.

•	Using graph assemblies is also a possibility, however the computational cost is excessive, making it unsuitable for high-throughput data analysis, and it is not available as an easily accessible option (Galaxy). Moreover, the benefits of such an approach for RE analysis have not yet been studied. Given the success of RepEnTools in its present form, it is unlikely that the small margin of improvement still possible will justify the cost. Finally, pseudoalignments result in false positives, while de novo RE discovery from the reads themselves is costly and inefficient, see Goerner-Potvin P and Bourque G, 2018.

•	MAPQ is unsuitable to analyse reads for REs. A low alignment score may come from a. inadequate search for better matches within the assembly, b. divergence from the reference assembly specific to the source of the genomic material, c. sequencing artefacts, d. bona fide bad alignment. Additionally, essentially all alignment software intentionally reduce the MAPQ score of multi-mapping reads.

### Biological considerations    
•	Some REs are highly similar, or only diverge in a specific part of their sequence. Repeat masker developed specialised strategies to accommodate this and accelerate processing (repeatmasker.org/webrepeatmaskerhelp). However, the annotation output does not reflect that. Thus, RepEnTools cannot take that into consideration as it is essentially an issue of the annotation. Nevertheless, as we demonstrated using simulated data, the strategies we employ in RepEnTools result in very good performance for the overwhelming majority of the REs. We highly recommend consulting dfam.org for comparisons of consensus sequence similarity for REs of interest. Similarly, it is advisable to consult specialised literature regarding RE sequence evolution and homology.

•	Investigating groupings that are too diverse will likely result in dilution of the enrichment/depletion. Similarly, the epigenetic marks of some REs, such as the TAR, are locus dependent despite insignificant sequence differences. Thus, groupings should be carefully selected and results should be assessed critically. As always, interpretation of any results should be done with appropriate care.
