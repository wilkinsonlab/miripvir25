#!/bin/bash
# Copies and inflates the file. We use pigz to speed it up.

pigz -d -c -p8 {{path}}/{{input_read1}} > {{product['output_read1']}}
pigz -d -c -p8 {{path}}/{{input_read2}} > {{product['output_read2']}}

