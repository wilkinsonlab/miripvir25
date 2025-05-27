import pandas as pd
from miripvir.filters import blast_filter, blast_filter_lc
from miripvir.data import LookUpTable, BlastPairedEndReads
from miripvir.ioutils import read_paired_end_files, read_blastdb_reference, read_single_end_files
import click
import logging
import taxoniq
from Bio import SeqIO
import numpy as np
import tqdm

logging.basicConfig(level=logging.DEBUG)
cli = click.Group()

def convert_to_fasta(taxid, index, sequence):
    return f">{taxid}_{index}\n{sequence}"
        
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

def extract_sequences(file):
    """
        
    """
    with open(file, 'r') as f:
        sequences = SeqIO.parse(f, format='fasta')
        sequences = [dict(id=item.id, sequence=str(item.seq)) for item in sequences]
    return sequences


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
@click.option("--query_coverage", "-q", default=100.0, help="Percentage of the query that should be spanned by the mapped fragments.")
@click.option("--length_threshold", "-l", default=125, help="Length of the mapped sequence.")
@click.option("--library_name", "-n", default="sample", help="Name of the library, useful to concatenate outputs from many samples")
@click.option("--count_threshold", "-t", default=10, help="Count threshold to output an OTU")
@click.option("--remove_prefix", "-r", default=False, help="")
@click.argument("hits1")
@click.argument("reference")
@click.argument("output")
def filter_blast_lc(
    hits1, output, reference, 
    library_name, query_coverage, length_threshold,
    count_threshold, remove_prefix
):
    """
    Applies a protocol for filtering BLAST hits similar to what
    was implemented in McLeish2024, but on single end reads. 
    See the Notes section for more details.

    Args:
        hits: Sequencing reads.
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
    reads = read_single_end_files(hits1)
    reference = read_blastdb_reference(reference)
    hits = blast_filter_lc(
        reads=reads, library_name=library_name,
        query_coverage=query_coverage, length_threshold=length_threshold,
        lookup_table=reference
    )
    hits.query(f"count > {count_threshold}").to_csv(output, sep='\t')


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


# @click.command()
# @click.argument("FILE")
# @click.argument("GTDB_PATH")
# def catalogue_gtdb(file, gtdb_path):
#     """
#     Args:
#         file: text file including the identifiers of the genomes that will be used for metagenomic simulation.
#         gtdb_path: path to gtdb genomes location. This should be the result of downloading the XXX file from GTDB FTP server.
#     """
#     entries = pd.read_csv(file)

#     metadata = pd.read_csv(gtdb_path + "/bac120_metadata_r220.tsv", sep="\t")    
#     paths = pd.read_csv(gtdb_path + "/genome_paths.tsv", sep="\t", header=None, names=['filename', 'path'])
#     paths['genome'] = paths['filename'].apply(lambda x: x.replace("_genomic.fna.gz", ""))
#     paths = paths.set_index("genome")
#     for item in entries.iterrows():
#         u = metadata.query('ncbi_taxid == "{0}"'.format(item.ncbi))
#         if len(u) == 0:
#             logging.warning("entry {0} did not have any entry in gtdb".format(item.ncbi))
#             continue
#         accession = u.accession # TODO Change this to the right colum
#         accession_path = paths.loc[accession]
#         sequences = extract_sequences(gtdb_path + '/' + accession_path.path + '/' + accession.filename)


@click.command()
@click.argument("DB")
@click.argument("PRODUCT")
def db_to_fasta(db, product):
    """
    Converts the database info, stored in the JSON file, into a FASTA file for sequence simulation.
    """
    sequence_db = pd.read_json(db)
    fasta = sequence_db[['taxid', 'index', 'sequence']].apply(lambda x: convert_to_fasta(x['taxid'], x['index'], x['sequence']), axis=1).to_list()
    with open(product + '.fasta', 'w') as f:
        f.write('\n'.join(fasta))


@click.command()
@click.option("--host_taxon_id", '-x', default=3702, help="host taxon identifier. It should be available in the DB")
@click.option("--host_abundance", '-b', default=0.90, help="Must be lower than 1.0")
@click.option("--mean", "-m", default=0.5, help="mean of the lognormal distribution")
@click.option("--sigma", "-s", default=2.0, help="variance of the lognormal distribution")
@click.argument("DB")
@click.argument("PRODUCT")
def simulate_abundance(db, product, host_taxon_id, host_abundance, mean, sigma):
    """

    """
    logging.debug(f"Host Abundance: {host_abundance}")
    others_abundance = 1 - host_abundance
    sequence_db = pd.read_json(db)
    logging.debug("computing sequence lengths")
    sequence_db['weight'] = sequence_db['sequence_length'] / sequence_db['length']
    logging.debug("separating host and other taxa")
    host = sequence_db[sequence_db.taxid == host_taxon_id].copy()
    others = sequence_db[sequence_db.taxid != host_taxon_id].copy()
    host['abundance'] = host['weight'] * host_abundance
    others_s = others[['taxid']].drop_duplicates('taxid')
    others_s['r'] = np.random.lognormal(mean=mean, sigma=sigma, size=len(others_s))
    others_s['r'] = others_s['r'] / others_s['r'].sum()
    others = pd.merge(others, others_s, on='taxid')
    others['abundance'] = others['r'] * others['weight'] * others_abundance
    logging.debug("merging")
    sampling_df = pd.concat((host[['taxid', 'index', 'abundance', 'sequence']], others[['taxid', 'index', 'abundance', 'sequence']]))
    sampling_df['abundance'] = sampling_df['abundance'] / sampling_df['abundance'].sum()
    sampling_df['index_name'] = sampling_df.apply(lambda x: "{0}_{1}".format(x['taxid'], x['index']), axis=1)
    logging.debug("writing")
    sampling_df[['index_name', 'abundance']].to_csv(product + '.abundances.txt', sep='\t', header=None, index=None)



@click.command()
@click.option('--domains', '-d', multiple=True, help="filter domains out of the sample. Use -d unknown to keep unclassified sequences")
@click.argument("FILE")
@click.argument("OUTPUT")
def kraken_filter(file, output, domains):
    """
    Creates a list of sequence ids to be kept out of a Kraken2 analysis.
    """
    kraken2_out = pd.read_csv(file, sep="\t", header=None, index_col=None, names=['is_classified', 'seq_id',  'taxonid', '_1', '_2'])
    taxonomy = []
    for item in tqdm.tqdm(kraken2_out['taxonid'].unique()):
        try:
            t = taxoniq.Taxon(item)
            domain = t.ranked_lineage[-1].scientific_name
            kingdom = t.ranked_lineage[-2].scientific_name
        except KeyError:
            taxonomy.append(dict(taxonid=item, species_name="unknown", domain="unknown", kingdom="unknown"))
            continue
        except IndexError:
            taxonomy.append(dict(taxonid=item, species_name=t.scientific_name, domain="unknown", kingdom="unknown"))
            continue
        taxonomy.append(
            dict(
                taxonid=item, 
                species_name=t.scientific_name,
                domain=domain,
                kingdom=kingdom
            )
        )
    taxonomy = pd.DataFrame.from_records(taxonomy)
    kraken2_out = pd.merge(kraken2_out, taxonomy, on='taxonid')
    kraken2_out[
        kraken2_out['domain'].isin(domains)
    ][['seq_id']].to_csv(output, sep="\t", index=None, header=None)


cli.add_command(filter_blast)
cli.add_command(filter_blast_lc)
cli.add_command(kraken2otus)
cli.add_command(simulate_abundance)
cli.add_command(db_to_fasta)
cli.add_command(kraken_filter)
if __name__ == "__main__":
    cli()