#!/bin/bash
# Trims adapters and cuts regions with low quality

fastp -i {{upstream['copy']['output_read1']}} \
    -I {{upstream['copy']['output_read2']}} \
    -a {{primers}} \
    -q {{quality_threshold}} \
    -w {{threads}} \
    -o {{product['output_read1']}} -O {{product['output_read2']}} > {{product['log']}}