#!/bin/bash
rm "{{upstream['copy']['output_read1']}}"
rm "{{upstream['copy']['output_read2']}}"
rm "{{upstream['quality']['output_read1']}}"
rm "{{upstream['quality']['output_read2']}}"

echo "done" >> {{product}}