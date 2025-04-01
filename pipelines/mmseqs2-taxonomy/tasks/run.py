import pandas as pd
import taxoniq

def features(product, upstream):
    """Join raw data with generated features
    """
    kraken2_out = pd.read_csv(upstream['filter-host'], sep="\t", header=None, index_col=None, names=['is_classified', 'seq_id',  'taxonid', '_1', '_2'])
    kraken2_out[:10]
