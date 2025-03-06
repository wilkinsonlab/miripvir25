#!/bin/bash
magicblast -query {{upstream['quality']['output_read1']}} \
    -query_mate {{upstream['quality']['output_read2']}} \
    -db {{blastdb}} -infmt fastq -outfmt tabular \
    -num_threads {{threads}}  -no_unaligned -perc_identity 100 > {{product['hits']}}
