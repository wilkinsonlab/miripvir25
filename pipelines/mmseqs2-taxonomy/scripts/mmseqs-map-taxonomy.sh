#!/bin/bash
echo {{upstream['mmseqs-create-db']['log']}}
mmseqs2 taxonomy {{upstream['mmseqs-create-db']['db']}} {{ref_db_path}} {{name}} tmp -s 2 > {{product['log_search']}}
mmseqs2 createtsv {{upstream['mmseqs-create-db']['db']}} {{name}} {{product['tsv']}} > {{product['log_tsv']}}
mmseqs2 taxonomyreport {{upstream['mmseqs-create-db']}} {{name}} {{product['html']}} --report-mode 1  > {{product['log_report']}}