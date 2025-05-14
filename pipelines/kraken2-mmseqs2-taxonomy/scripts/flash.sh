#!/bin/bash
# --- 
flash -t {{threads}} \
    {{upstream['remove-host']['output_read1']}} \
    {{upstream['remove-host']['output_read2']}} > {{product['log']}}
# --- 
mv out.extendedFrags.fastq {{product['output_contig']}}
rm out.hist
rm out.histogram
rm out.notCombined_1.fastq
rm out.notCombined_2.fastq