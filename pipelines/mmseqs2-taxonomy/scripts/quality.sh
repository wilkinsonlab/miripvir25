#!/bin/bash
# Trims adapters and cuts regions with low quality
primers="{{primers}}"
if [ -z "${primers}" ]; then
    fastp -i {{input_read1}} \
        -I {{input_read2}} \
        -q {{quality_threshold}} \
        -w {{threads}} \
        -o {{product['output_read1']}} -O {{product['output_read2']}} > {{product['log']}}

else
    fastp -i {{input_read1}} \
        -I {{input_read2}} \
        -a {{primers}} \
        -q {{quality_threshold}} \
        -w {{threads}} \
        -o {{product['output_read1']}} -O {{product['output_read2']}} > {{product['log']}}
fi