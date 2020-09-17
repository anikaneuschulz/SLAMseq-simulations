import pysam
import pdb
import random
import sys

## this labels reads of given genes at given frequencies
## genes have to be goven in a text file of the following format:
## <EMSBL gene ID>\t<labeling eff>\n

if len(sys.argv) == 3:
    ifn = sys.argv[1]
    genes_file = sys.argv[2]
else:
    print("Please make my life easier by providing an input file (indexed .bam) with ENSMBL IDs in the XT tag and a list of genes to be labeled with the desired labeling frequencies in % (one gene per line, format: ENSMBL ID <tab> labeling eff).")
    sys.exit()


bamfile = pysam.AlignmentFile(ifn, "rb")

ofn = ifn[:-4] + "_labeled_per_gene" + ".sam"

labeledfile = pysam.AlignmentFile(ofn, "w", template=bamfile)

desired_genes_dict = {}

genes = open(genes_file, "r")

#pdb.set_trace()

for line in genes:
    l = line.rstrip().split("\t")
    if not l[0] in desired_genes_dict:
        desired_genes_dict[l[0]] = l[1]

for read in bamfile.fetch():
    if read.has_tag("XT"):
        gene = read.get_tag("XT")
        if gene in desired_genes_dict:
            eff = int(desired_genes_dict[gene])
            random.seed()
            if read.is_reverse:
                orig_base = "A"
                target = "G"
            else:
                orig_base = "T"
                target = "C"
            sequence = list(read.seq)
            for pos in range(len(sequence)):
                if sequence[pos] == orig_base:
                    try:
                        x = random.random()*100
                        if x <= eff:
                            sequence[pos] = target
                    except IndexError:
                        pass
            quality_saver = read.qual
            read.seq = "".join(sequence)
            read.qual = quality_saver
            labeledfile.write(read)
        else:
            labeledfile.write(read)
    else:
        labeledfile.write(read)

print("done. Saving file as", ofn)
labeledfile.close()
