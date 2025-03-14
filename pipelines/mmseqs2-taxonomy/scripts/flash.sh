#!/bin/bash
# --- 
flash -t {{threads}} \
    {{upstream['quality']['output_read1']}} \
    {{upstream['quality']['output_read2']}}
# --- 
mv out.extendedFrags.fastq {{product}}
rm out.hist
rm out.histogram
rm out.notCombined_1.fastq
rm out.notCombined_2.fastq