#!/usr/bin
cd {{path}}
cat {{upstream['download']['success']}}  | tail -n +2 | xargs -I % cat %.fna > genomes.fna
makeblastdb -dbtype nucl -in genomes.fna -parse_seqids -input_type fasta -title "{{dbname}}" -out "{{dbnamepath}}"
cat genomes.fna | grep '>' | sed 's/>//g' > {{product['index']}}
rm genomes.fna 