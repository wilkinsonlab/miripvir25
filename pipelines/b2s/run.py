import pandas as pd
from miripvir.filters import blast_filter
from miripvir.data import LookUpTable, BlastPairedEndReads
from miripvir.ioutils import read_paired_end_files, read_blastdb_reference

def filter_blast(
    upstream, product, library_name, query_coverage,
    length_threshold, lookup_table
):
    """
    Just wraps ´miripvir.filters.blast_filter´ into ploomber

    """

    reads = read_paired_end_files(
        file_forward=upstream['blast-map']['output_read1'],
        file_backward=upstream['blast-map']['output_read2']
    )
    lookup_table = read_blastdb_reference(lookup_table)
    
    hits = blast_filter(
        reads=reads, library_name=library_name,
        query_coverage=query_coverage, length_threshold=length_threshold,
        lookup_table=lookup_table
    )
    hits.to_csv(product['species_hits'], sep=';')
