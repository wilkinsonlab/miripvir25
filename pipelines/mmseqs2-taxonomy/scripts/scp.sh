#!/bin/bash
# Copies and inflates the file. We use pigz to speed it up.
scp "{{user}}@{{url}}:{{remote_path}}/{{input_read1}}" . 
file="{{input_read1}}"
if [ "${file: -3}" == ".gz" ]; then
    pigz -d -c -p8 {{input_read1}} > {{product['output_read1']}}
elif [ "${file: -4}" == ".zip" ]; then
    unzip -p {{input_read1}} > {{product['output_read1']}}
fi
rm {{input_read1}}

scp "{{user}}@{{url}}:{{remote_path}}/{{input_read2}}" . 
file="{{input_read2}}"
if [ "${file: -3}" == ".gz" ]; then
    pigz -d -c -p8 {{input_read2}} > {{product['output_read2']}}
elif [ "${file: -4}" == ".zip" ]; then
    unzip -p {{input_read2}} > {{product['output_read2']}}
fi
rm {{input_read2}}