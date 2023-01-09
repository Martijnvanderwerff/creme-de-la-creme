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
database=ncbi

kraken2-build --download-taxonomy --db ${workdir}kraken2-db-ncbi
kraken2-build --add-to-library ${workdir}16S-genomes/bacteria.16SrRNA.fna --db /students/2022-2023/master/creme_de_la_creme/kraken2/kraken2-db-${database} --threads 16
kraken2-build --build --db /students/2022-2023/master/creme_de_la_creme/kraken2/kraken2-db-${database} 