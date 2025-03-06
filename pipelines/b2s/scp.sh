#!/bin/bash
# Copies and inflates the file. We use pigz to speed it up.
scp "{{user}}@{{url}}:{{remote_path}}/{{input_read1}}" . 
pigz -d -c -p8 {{input_read1}} > {{product['output_read1']}}
scp "{{user}}@{{url}}:{{remote_path}}/{{input_read2}}" . 
pigz -d -c -p8 {{input_read2}} > {{product['output_read2']}}
rm {{input_read1}}
rm {{input_read2}}