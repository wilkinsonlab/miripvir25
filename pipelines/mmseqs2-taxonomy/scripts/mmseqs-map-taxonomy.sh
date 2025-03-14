#!/bin/bash
alias mmseqs='docker pull ghcr.io/soedinglab/mmseqs2'
mmseqs taxonomy {{upstream['mmseqs-create-db']}} {{ref_db_path}} {{name}} tmp -s 2
mmseqs createtsv {{ref_db_path}} {{name}} {{product['tsv']}}
mmseqs taxonomyreport {{upstream['mmseqs-create-db']}} {{name}} {{product['html']}} --report-mode 1