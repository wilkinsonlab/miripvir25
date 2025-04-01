#!/bin/bash

seqkit fq2fa -o read1.fasta {{upstream['quality']['output_read1']}}

blastn -db {{blastdb}} -evalue {{evalue}} \
    -out {{product['output_read1']}} -query read1.fasta -num_threads {{threads}} \
    -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen qcovs"

rm read1.fasta

seqkit fq2fa -o read2.fasta {{upstream['quality']['output_read2']}}

blastn -db {{blastdb}} -evalue {{evalue}} \
    -out {{product['output_read2']}} -query read2.fasta -num_threads {{threads}} \
    -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen qcovs"

rm read2.fasta