import pandas as pd
import taxoniq
import click
import sys

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
@click.option("-o", "--output", default=None)
@click.option("-l", "--library", default="none")
@click.argument("FILE")
def summarize(file, output, library):
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
    df['classification-ratio'] = len_classified_df / len_raw_df
    df['scientific_name'] = df['taxonid'].apply(obtain_scientific_name)
    df['library'] = library
    if output is not None:
        df[['library', 'taxonid', 'scientific_name', 'count']].to_csv(output, index=None)
    else:
        print(df[['library', 'classification-ratio', 'taxonid', 'scientific_name', 'count']].to_csv(sep=",", index=None), end="")

if __name__ == "__main__":
    summarize()