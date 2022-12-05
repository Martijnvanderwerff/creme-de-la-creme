# This bash script will run minimap2 on barcorde 10 FastQ files (pulled into one FASTA file)
# SLURM is used as a workload manager

#!/bin/bash
#SBATCH --job-name=minimap-2
#SBATCH --time=15:00:00
#SBATCH --ntasks=1
#SBATCH --mem=150GB
#SBATCH --cpus-per-task=17
#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.w.van.der.werff@st.hanze.nl
#SBATCH --mail-type=BEGIN,FAIL,END
#SBATCH --partition=assemblix

workdir=/students/2022-2023/master/creme_de_la_creme/

# Check for human genes
minimap2 -ax splice -uf -k14 -t 16 ${workdir}hg38.fa ${workdir}example_16S/barcode10/test.fa > ${workdir}minimap2-test/human-aln.sam