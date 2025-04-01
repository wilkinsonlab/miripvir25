#!/bin/bash
# Trims adapters and cuts regions with low quality

# cutadapt -q {{quality_threshold}} -a {{primers}} \
#     -o {{product['output_read1']}} \
#     {{upstream['copy']['output_read1']}}


# cutadapt -q {{quality_threshold}} -a {{primers}} \
#     -o {{product['output_read2']}} \
#     {{upstream['copy']['output_read2']}}


fastp -i {{upstream['copy']['output_read1']}} \
    -I {{upstream['copy']['output_read2']}} \
    -a {{primers}} \
    -q {{quality_threshold}} \
    -w {{threads}} \
    -o {{product['output_read1']}} -O {{product['output_read2']}}