import pandas as pd
from miripvir.filters import blast_filter
from miripvir.data import LookUpTable, BlastPairedEndReads
from miripvir.ioutils import read_paired_end_files, read_blastdb_reference
import click
import logging
import taxoniq

logging.basicConfig(level=logging.DEBUG)
cli = click.Group()

def obtain_level(taxonid, level):
    try:
        return list(reversed(taxoniq.Taxon(taxonid).ranked_lineage))[level].scientific_name
    except IndexError:
        return "unknown"
    except KeyError:
        return "unknown"

def obtain_scientific_name(taxonid):
    try:
        return taxoniq.Taxon(taxonid).scientific_name
    except IndexError:
        return "unknown"
    except KeyError:
        return "unknown"



@click.command()
@click.option("--query_coverage", "-q", default=100.0, help="Percentage of the query that should be spanned by the mapped fragments.")
@click.option("--length_threshold", "-l", default=125, help="Length of the mapped sequence.")
@click.option("--library_name", "-n", default="sample", help="Name of the library, useful to concatenate outputs from many samples")
@click.option("--count_threshold", "-t", default=10, help="Count threshold to output an OTU")
@click.option("--remove_prefix", "-r", default=False, help="")
@click.argument("hits1")
@click.argument("hits2")
@click.argument("reference")
@click.argument("output")
def filter_blast(
    hits1, hits2, output, reference, 
    library_name, query_coverage, length_threshold,
    count_threshold, remove_prefix
):
    """
    Applies a protocol for filtering BLAST hits similar to what
    was implemented in McLeish2024. See the Notes section for more details.

    Args:
        hits1: Forward sequencing reads.
        hits2: Forward sequencing reads.
        reference: Table connecting the IDs of the mapping sequences with the accession and taxids
        

    Returns:
        Filtered and grouped OTUs and their associated read count. 


    Notes:

        This command enables a complex pipeline with different steps. These ones
        are bundled together in this script to ease testing.
        1. Remove mapped sequences with lengths under length_threshold
        2. Remove mapped sequences with query coverages under query_coverage
        3. Remove sequences whose paired ends did not align to the same reference sequences
        4. Remove sequences whose alignment is ambiguous (e.g. mapping to two different locations)
        5. Group all results by species hits
    """
    reads = read_paired_end_files(
        file_forward=hits1,
        file_backward=hits2
    )
    reference = read_blastdb_reference(reference)
    hits = blast_filter(
        reads=reads, library_name=library_name,
        query_coverage=query_coverage, length_threshold=length_threshold,
        lookup_table=reference, remove_prefix=remove_prefix
    )
    hits.hits.query(f"count > {count_threshold}").to_csv(output, sep='\t')


@click.command()
@click.option("-n", "--library_name", default="none")
@click.option("--count_threshold", "-t", default=10, help="Count threshold to output an OTU")
@click.argument("FILE")
@click.argument("OUTPUT")
def kraken2otus(file, output, library_name, count_threshold):
    """

    Maps the Kraken2 output to a list of taxon - number of sequences, 
    which should be much easier to handle for later analysis than the mere
    kraken2 output. 

    """
    df = pd.read_csv(file, sep="\t", header=None, index_col=None, names=['is_classified', 'seq_id',  'taxonid', '_1', '_2'])
    len_raw_df = len(df)
    df = df.query('is_classified == "C"').copy()
    len_classified_df = len(df)
    df = df.value_counts(['taxonid']).reset_index()

    classification_ratio = len_classified_df / len_raw_df

    logging.info(f"classification ratio = {classification_ratio:6.5f}")

    df['classification-ratio'] = classification_ratio
    df['scientific_name'] = df['taxonid'].apply(obtain_scientific_name)
    df['library'] = library_name
    df = df.query(f'count > {count_threshold}')
    df[['library', 'classification-ratio', 'taxonid', 'scientific_name', 'count']].to_csv(output, index=None)


cli.add_command(filter_blast)
cli.add_command(kraken2otus)
if __name__ == "__main__":
    cli()