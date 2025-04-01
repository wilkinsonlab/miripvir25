# %% tags=["parameters"]
upstream = ['map']
product = None
library_name = None
identity_threshold = None
length_threshold = None
species_reference = None
# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
##
genome_index = pd.read_json(species_reference)
##
def read_hits_tab(file, library):
    """
    Arguments
    ---
    - file: File from where to read the input
    - library: Provides a name to the library
    """
    hits = pd.read_csv(
        file, 
        sep="\s+", comment='#', header=None
    )
    hits.columns=[
        'query_id', 'ref_id', 'identity', '_', '_', '_', 'qstart', 'qend', 'rstart', 'rend', 
        '_', '_', 'score', 'qstrand', 'rstrand', 'qrlength', 'BTOP', 'difaln', '_', '_',
        '_', 'unaligned', '_', '_', '_'
    ]
    hits = hits[['query_id', 'ref_id', 'identity','qstart', 'qend', 'rstart', 'rend', 'score', 'qstrand', 'rstrand', 'qrlength', 'difaln']]
    hits['library'] = library
    return hits
## 
hits = read_hits_tab(upstream['map']['hits'], library_name)
##
hits_taxid = pd.merge(
    hits, genome_index, 
    right_on='sequence_id', left_on='ref_id'
)
hits_taxid = hits_taxid.query(f'identity == {identity_threshold}')
hits_taxid['aln_len'] = hits_taxid['qend'] - hits_taxid['qstart']
hits_taxid = hits_taxid.query(f'aln_len > {length_threshold}')
hits_taxid = hits_taxid.query(f'difaln < 2')
hits_taxid
##
hits_taxid_dd = hits_taxid.drop_duplicates(subset=['query_id', 'sequence_id'], keep='first')
hits_taxid_dd
##
sns.displot(hits_taxid_dd, x='aln_len', bins=20)
##
hits_taxid_dd_by_taxid =  hits_taxid_dd.value_counts(
    subset=['taxid', 'query_id']
).reset_index()
hits_taxid_dd_by_taxid
##
hits_taxid_dd_unambiguous_ids = hits_taxid_dd_by_taxid.value_counts(
    subset=['query_id']
).reset_index()# .query('count < 2')['query_id'].to_list()

hits_taxid_dd_unambiguous_ids
## 
selected_hits = hits_taxid_dd_unambiguous_ids.query('count < 2')['query_id'].to_list()
##
species_hits = pd.merge(
    hits[hits['query_id'].isin(selected_hits)], genome_index[['sequence_id', 'organism', 'taxid']], 
    right_on='sequence_id', left_on='ref_id'
).value_counts(subset=['organism', 'taxid']).reset_index()
##
species_hits['log_count'] = species_hits['count'].apply(np.log10)
g = sns.catplot(y='organism', x='log_count', data=species_hits, aspect=0.4, height=12.0)
##
species_hits.to_json(
    product['species_hits'],
    orient='records', indent=4
)
