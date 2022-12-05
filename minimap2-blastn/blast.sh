#!/bin/bash
#SBATCH --job-name=blastn
#SBATCH --ntasks=1
#SBATCH --mem=150GB
#SBATCH --cpus-per-task=17
#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.w.van.der.werff@st.hanze.nl
#SBATCH --mail-type=BEGIN,FAIL,END
#SBATCH --partition=assemblix

source /commons/conda/conda_load.sh
conda activate /students/2022-2023/master/creme_de_la_creme/conda-envs/blast

workdir=/students/2022-2023/master/creme_de_la_creme/

blastn -query ${workdir}example_16S/barcode10/test.fa -db /data/datasets/NCBI/BLASTDB/16S_ribosomal_RNA \
-outfmt '6 qseqid saccver pident length mismatch gapopen qstart qend sstart send evalue bitscore sscinames' \
-out ${workdir}output-blastn/barcode10.txt -num_alignments 1