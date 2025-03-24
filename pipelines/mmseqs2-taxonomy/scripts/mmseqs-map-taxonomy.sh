#!/bin/bash
echo {{upstream['mmseqs-create-db']['log']}}
mmseqs taxonomy {{upstream['mmseqs-create-db']['db']}} {{ref_db_path}} {{name}} tmp -s 2 --split-memory-limit 128GB > {{product['log_search']}}
mmseqs createtsv {{upstream['mmseqs-create-db']['db']}} {{name}} {{product['tsv']}} > {{product['log_tsv']}}
mmseqs taxonomyreport {{ref_db_path}} {{name}} {{product['html']}} --report-mode 1  > {{product['log_report']}}
