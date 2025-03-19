#!/bin/bash
seqtk subseq {{upstream['quality']['output_read1']}} {{upstream['filter-host']['csv']}} > {{product['output_read1']}}
seqtk subseq {{upstream['quality']['output_read1']}} {{upstream['filter-host']['csv']}} > {{product['output_read2']}}
echo "ls -la {{product['output_read1']}}" > {{product['log']}}
echo "ls -la {{product['output_read2']}}" >> {{product['log']}}