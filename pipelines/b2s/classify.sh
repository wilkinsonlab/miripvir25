k2 classify \
     --paired  \
     --db {{ kraken_db }} \
     --output {{ product['kraken_out'] }} \
     --threads {{ kraken_threads }} \
     {{ upstream['quality']['output_read1'] }} {{ upstream['quality']['output_read2'] }}