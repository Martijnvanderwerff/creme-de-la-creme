#!/bin/bash

output=/students/2022-2023/master/creme_de_la_creme/

wget -P ${output} http://hgdownload.cse.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
gzip -d ${output}/hg38.fa.gz