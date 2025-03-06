k2 classify --db {{ kraken_db }} --output {{ product['kraken_out'] }} --paired  --threads {{ kraken_threads }} \
     {{ upstream['clean']['output_read1'] }} {{ upstream['clean']['output_read2'] }}