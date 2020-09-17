SLAMseq simulation scripts
--

This repository contains python scripts to simulate SLAMseq data based on real, unlabeled RNAseq data. The data generated can be utilized to e.g. test analysis pipelines or set up computational workflows.

Required libraries: Pysam, random

Input needs to be a mapped, sorted and indexed .bam file.  
Output is given in a .sam file.

Instructions can be obtained be calling each script without any arguments.

**label_bam_mappingPosUNaware.py** adds labeling events to the whole inuput file according to the labeling probability (in %, no decimals) given.  

**label_bam_per_gene_MappingPosUNaware_AllReadsOut_v1.py** adds labeling events only to specified genes ad given probabilities. Gene identifiers need to be given in the XT tag (created through e.g. Rsubread - https://bioconductor.org/packages/release/bioc/html/Rsubread.html) - or adapt the script to the tag needed.  
gene identifiers (e.g. ENSMBL IDs) and desired labeling probabilities (in %, no decimals) have to be given in a text file of the following format:  
```<gene identifier>\t<labeling eff>\n```
