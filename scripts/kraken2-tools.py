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
@click.option("-o", "--output-hits", default=None)
@click.option("-c", "--output-counts", default=None)
@click.argument("FILE")
def summarize(file, output_hits, output_counts):
    
    u = dict()
    df = pd.read_csv(file, sep="\t", header=None, index_col=None, names=['is_classified', 'seq_id',  'taxonid', '_1', '_2'])
    len_raw_df = len(df)
    df = df.query('is_classified == "C"').copy()
    len_classified_df = len(df)
    df = df.value_counts(['taxonid']).reset_index()
    u['classification-ratio'] = len_classified_df / len_raw_df
    df['scientific_name'] = df['taxonid'].apply(obtain_scientific_name)
    df['level_0'] = df['taxonid'].apply(lambda x: obtain_level(x, 0))
    df['level_1'] = df['taxonid'].apply(lambda x: obtain_level(x, 1))
    df['level_2'] = df['taxonid'].apply(lambda x: obtain_level(x, 2))
    df['level_3'] = df['taxonid'].apply(lambda x: obtain_level(x, 3))
    if output_hits is not None:
        df.value_counts(subset=['level_0', 'level_1', 'level_2', 'level_3']).reset_index().to_csv(output_hits, index=None)
    if output_counts is not None:
        df[
            ['level_0', 'level_1', 'level_2', 'level_3', 'count']
        ].groupby(['level_0', 'level_1', 'level_2', 'level_3'], as_index=False).sum().to_csv(output_counts, index=None)

if __name__ == "__main__":
    summarize()