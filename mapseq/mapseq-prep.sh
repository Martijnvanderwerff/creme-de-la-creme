data_dir = "/students/2022-2023/master/creme_de_la_creme/"

# Generates multifasta from multiple FastQ files, example for barcode10 folder
cat ${data_dir}example_16S/*.fastq \
| paste - - - - | sed 's/^@/>/g'| cut -f1-2 | tr '\t' '\n' \
> ${data_dir}example_16S/barcode10/test.fa

# Runs mapseq after correcly installing the software from Github
${data_dir}mapseq-test/mapseq-1.2.6-linux/mapseq \
${data_dir}example_16S/barcode10/test.fa > barcode20-mapseq.mseq
