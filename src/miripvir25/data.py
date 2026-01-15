import pandas as pd
import taxoniq
import os
import gzip
import shutil
from urllib.request import urlopen


def fault_tolerant_rank(x: int):
    """
    Searches in the taxoniq database for a given taxon identifier, and 
    returns the corresponding rank. If it does not find it, it provides a Pandas NaN. 
    Useful to filter Kraken2 results in Pandas. 
    
    :param x: Taxon Identifier
    :type x: int
    """
    try:
        return taxoniq.Taxon(x).rank.name
    except KeyError:
        return pd.NA


def load_mmseqs2(file, label, method):
    """
    assigning labels from reading https://mmseqs.com/latest/userguide.pdf, taxonomy output and TSV
    """
    df = pd.read_csv(
        file, 
        sep='\t', 
        header=None, 
        index_col=None,
        names=['seq_id', 'taxid', 'level', 'species_name', 'fragments', 'frag_labeled', 'agreement', 'support']
    )
    # df = df[['library', 'seq_id', 'taxid', 'level', 'species_name', 'fragments', 'support', 'method']]
    df = df.query('level == "species"').value_counts(['taxid', 'species_name']).reset_index().rename(columns={'species_name':'scientific_name'}).copy()
    df['label'] = label
    df['method'] = method
    df = df[['taxid', 'label', 'method', 'scientific_name', 'method']]
    return df


def load_kraken2(file, label, method):
    df = pd.read_csv(file, sep=',', index_col=None)
    df = df.rename(columns={'library': 'method', 'taxonid': 'taxid'}).drop(columns=['classification-ratio'])
    df['rank'] = df['taxid'].apply(fault_tolerant_rank)
    df = df.dropna(subset=['rank']).query('rank == "species"').drop(columns=['rank']).copy()
    df['method'] = method
    df['ncbi_taxid'] = df['taxid']
    df = df[['taxid', 'ncbi_taxid', 'method', 'scientific_name']]
    df['label'] = label
    return df


def load_motus(file, label, method): 
    df = pd.read_csv(file, sep="\t", comment='#', header=None, names=['otu', 'scientific_name', 'taxid', 'count'])
    df['label'] = label
    df['method'] = method
    return df

def load_metaphlan(file, label, method):
    df = pd.read_csv(file, comment='#', header=None, names=['clade', 'ncbi', 'abundance', '_'], sep='\t')
    df['label'] = label
    df['method'] = method 

    df['taxid'] = df['ncbi'].astype(str).apply(lambda x: x.split("|")[-1])
    df = df.query('taxid != ""').copy()
    df['taxid'] = df['taxid'].astype(int)
    df['rank'] = df['taxid'].apply(fault_tolerant_rank)
    df = df.dropna(subset=['rank']).query('rank == "species"').copy()
    return df
