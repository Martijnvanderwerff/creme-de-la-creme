#!/bin/bash
#SBATCH --job-name=kraken2
#SBATCH --time=06:00:00
#SBATCH --partition=assemblix
#SBATCH --ntasks=1
#SBATCH --nodes=1  
#SBATCH --cpus-per-task=16

source /commons/conda/conda_load.sh
conda activate /students/2022-2023/master/creme_de_la_creme/conda-envs/bracken

workdir=/students/2022-2023/master/creme_de_la_creme/kraken2/
barcodes=( 05 06 )

for barcode in "${barcodes[@]}"
do
  : 
  bracken -d ${workdir}kraken2-db-greengenes -i ${workdir}barcode${barcode}-greengenes/barcode${barcode}-greengenes.txt \
  -o ${workdir}barcode${barcode}-greengenes/barcode${barcode}-greengenes.bracken -r 1500
done
