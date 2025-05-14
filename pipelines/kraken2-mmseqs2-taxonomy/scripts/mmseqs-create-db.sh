#!/bin/bash
mmseqs createdb {{upstream['flash']['output_contig']}} {{product['db']}} > {{product['log']}}