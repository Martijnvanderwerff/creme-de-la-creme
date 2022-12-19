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

kraken2 --db ${workdir}kraken2-db-rdp --threads $SLURM_CPUS_PER_TASK --use-names --report ${workdir}barcode05-rdp/barcode05-rdp.txt \
${workdir}../fastq/pass/barcode05/*.fastq > ${workdir}barcode05-rdp/barcode05-rdp.kraken2
