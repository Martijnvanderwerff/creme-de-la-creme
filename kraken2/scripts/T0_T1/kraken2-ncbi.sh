#!/bin/bash
#SBATCH --job-name=kraken2-ncbi-16S
#SBATCH --time=06:00:00
#SBATCH --partition=assemblix
#SBATCH --ntasks=1
#SBATCH --nodes=1  
#SBATCH --cpus-per-task=16

source /commons/conda/conda_load.sh
conda activate /students/2022-2023/master/creme_de_la_creme/conda-envs/bracken

workdir=/students/2022-2023/master/creme_de_la_creme/
datadir=/students/2022-2023/master/creme_de_la_creme/Cream_T0_T1_161022/T0_T1/20221216_1224_MN36331_FAV77169_53689cad/fastq/pass/

mkdir ${workdir}/kraken2/T0_T1/ncbi

for barcode in $(seq -w 1 24)
do
  : 
  mkdir ${workdir}kraken2/T0_T1/ncbi/barcode${barcode}
  kraken2 --db ${workdir}/kraken2/kraken2-db-ncbi --threads $SLURM_CPUS_PER_TASK --use-names \
  --report ${workdir}kraken2/T0_T1/ncbi/barcode${barcode}/barcode${barcode}.txt \
  ${datadir}barcode${barcode}/*.fastq > ${workdir}kraken2/T0_T1/ncbi/barcode${barcode}/barcode${barcode}.kraken2
done
