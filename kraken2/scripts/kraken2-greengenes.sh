#!/bin/bash
#SBATCH --job-name=kraken2
#SBATCH --time=06:00:00
#SBATCH --partition=assemblix
#SBATCH --ntasks=1
#SBATCH --nodes=1  
#SBATCH --cpus-per-task=16

source /commons/conda/conda_load.sh
conda activate /students/2022-2023/master/creme_de_la_creme/conda-envs/kraken2

workdir=/students/2022-2023/master/creme_de_la_creme/kraken2/
barcodes=( 05 06 )

for barcode in "${barcodes[@]}"
do
  : 
  mkdir ${workdir}barcode${barcode}-greengenes
  kraken2 --db ${workdir}kraken2-db-greengenes --threads $SLURM_CPUS_PER_TASK --use-names --report ${workdir}barcode${barcode}-greengenes/barcode${barcode}-greengenes.txt \
  ${workdir}../fastq/pass/barcode${barcode}/*.fastq --output ${workdir}barcode${barcode}-greengenes/barcode${barcode}-greengenes.kraken2
done
