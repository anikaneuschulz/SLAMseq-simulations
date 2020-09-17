import pysam
import pdb
import random
import sys

## now with 100% less quality strings being lost!

# Author: Anika Neuschulz

if len(sys.argv) == 3:
    ifn = sys.argv[1]
    eff = int(sys.argv[2])
else:
    print("Please make my life easier by providing an input file (indexed .bam) and the desired labeling efficiancy in %.")
    sys.exit()

bamfile = pysam.AlignmentFile(ifn, "rb")

ofn = ifn[:-4] + "_labeledMapPosUnaware_" + str(eff) + ".sam"

labeledfile = pysam.AlignmentFile(ofn, "w", template=bamfile)

for read in bamfile.fetch():
    if read.is_reverse:
        orig_base = "A"
        target = "G"
    else:
        orig_base = "T"
        target = "C"
    random.seed()
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
labeledfile.close()
