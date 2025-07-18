import pandas as pd
import numpy as np


def simulate_lognormal_data(x, mean, sigma):
    """
    Generates an array of log-normally distributed 
    frequencies, so the total sum of the frequencies is
    still equal to 1. 

    """
    y = np.random.lognormal(
        mean=mean, 
        sigma=sigma, 
        size=x 
    )
    return y / y.sum()

def simulate_metatranscriptomic_abundance(db, fasta_file, abundance_file, mean, sigma, read_length=150):
    """
    """
    sequence_db = pd.read_json(db).query(f'sequence_length > {read_length}').copy()
    sequence_db['weight'] = sequence_db.groupby('taxid')['sequence_length'].transform(lambda x: x / x.sum())
    sequence_db['s'] = sequence_db.groupby(['taxid'], as_index=False).apply(lambda x: simulate_lognormal_data(len(x), 0.5, 2.0)).explode().values

    taxa = sequence_db[['taxid']].drop_duplicates('taxid')
    taxa['r'] = np.random.lognormal(
        mean=mean, 
        sigma=sigma, 
        size=len(taxa)
    )
    taxa['r'] = taxa['r'] / taxa['r'].sum()
    sequence_db = pd.merge(sequence_db, taxa, on='taxid')
    sequence_db['abundance'] = sequence_db['r'] * sequence_db['weight'] * sequence_db['s'] 
    sequence_db['abundance'] = sequence_db['abundance'] / sequence_db['abundance'].sum()
    fasta = sequence_db[['taxid', 'index', 'sequence']].apply(lambda x: convert_to_fasta(x['taxid'], x['index'], x['sequence']), axis=1).to_list()
    with open(fasta_file, 'w') as f:
        f.write('\n'.join(fasta))

    sequence_db['index_name'] = sequence_db.apply(lambda x: "{0}_{1}".format(x['taxid'], x['index']), axis=1)
    sequence_db[['index_name', 'abundance']].to_csv(abundance_file, sep='\t', header=None, index=None)
    

def convert_to_fasta(taxid, index, sequence):
    return f">{taxid}_{index}\n{sequence}"
