#!/bin/bash
iss generate --model HiSeq \
    --genomes "{{upstream['abundances']['fasta']}}" \
    --n_reads "{{reads}}" -p "{{cores}}" \
    --abundance_file "{{upstream['abundances']['abundances']}}" \
    -o tmp
# Removing the pair-end indicator to homogenize treatment
sed -i 's/\/1$//g' tmp_R1.fastq 
sed -i 's/\/2$//g' tmp_R2.fastq 
mv tmp_R1.fastq "{{product['output_R1']}}"
mv tmp_R2.fastq "{{product['output_R2']}}"
rm tmp*