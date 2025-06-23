#!/bin/bash
# cd {{path}}
# Define the file to read
file='{{upstream['accessions']['genome_accessions']}}'
echo "" > {{product['success']}}
echo "" > {{product['failures']}}
echo "" > {{product['log']}}
# Read the file line-by-line
while IFS= read -r line; do
  i=$(echo $line | awk  '{print $2}')
  echo -e "--- processing $line | $i " >> {{product['log']}}
  datasets download genome accession $i \
    --filename tmp.zip \
    --include cds 
  unzip -o {{path}}/tmp.zip
  rm -rf {{path}}/tmp.zip {{path}}/README.md {{path}}/md5sum.txt
  mv {{path}}/ncbi_dataset/data/${i}/*.fna ${i}.cds.fna && echo "$i" >> {{product['success']}} || echo "$i" >> {{product['failures']}}
  sleep 2
done < "$file"
rm -rf {{path}}/ncbi_dataset