source /commons/conda/conda_load.sh
conda activate /students/2022-2023/master/creme_de_la_creme/conda-envs/kraken2

workdir=/students/2022-2023/master/creme_de_la_creme/kraken2/

kraken2-build --db /students/2022-2023/master/creme_de_la_creme/kraken2/kraken2-db-${database} --special ${database} --threads 16