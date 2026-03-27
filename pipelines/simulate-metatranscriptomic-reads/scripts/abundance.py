import pandas as pd
import click
import logging
import taxoniq
import numpy as np
import tqdm

def convert_to_fasta(taxid, index, sequence):
    return f">{taxid}_{index}\n{sequence}"

@click.command()
@click.option("--host_taxon_id", '-x', default=3702, help="host taxon identifier. It should be available in the DB")
@click.option("--host_abundance", '-b', default=0.90, help="Must be lower than 1.0")
@click.option("--taxon_mean", "-m", default=0.5,)
@click.option("--taxon_sigma", "-s", default=2.0,)
@click.option("--cds_mean", "-n", default=0.5)
@click.option("--cds_sigma", "-t", default=2.0)
@click.option("--read_length", "-r", default=150)
@click.argument("DB")
@click.argument("PRODUCT")
def simulate_metranscriptomic_abundances_inhost(
    db, product, 
    host_taxon_id, host_abundance,
    taxon_mean, taxon_sigma, cds_mean, cds_sigma, 
    read_length
):
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
    # FILTERING SEQUENCES THAT ARE NOT LONGER THAN THE SIMULATED READ
    sequence_db = pd.read_json(db).query(f'sequence_length > {read_length}').copy()
    
    s_ = []

    for taxid in sequence_db.taxid.unique():
        sequence_db_taxid = sequence_db.query('taxid == {0}'.format(taxid))
        for value in simulate_lognormal_data(len(sequence_db_taxid), cds_mean, cds_sigma):
            s_.append(value)

    sequence_db['s'] = s_ 


    host = sequence_db[sequence_db.taxid == host_taxon_id].copy()
    others = sequence_db[sequence_db.taxid != host_taxon_id].copy()

    others = others[['taxid']].drop_duplicates('taxid')
    others['r'] = np.random.lognormal(
        mean=taxon_mean, 
        sigma=taxon_sigma, 
        size=len(others)
    )
    print("here!")
    others['r'] = (others['r'] / others['r'].sum()) * (1 - host_abundance)
    host = host.drop_duplicates('taxid')[['taxid']]
    host['r'] = host_abundance
    taxa = pd.concat([others, host])
    print("taxa: {:d}".format(len(taxa)))
    sequence_db = pd.merge(sequence_db, taxa, on='taxid')
    sequence_db['abundance'] = sequence_db['r'] * sequence_db['s'] 
    sequence_db['abundance'] = sequence_db['abundance'] / sequence_db['abundance'].sum()
    print("sequence_db is ready to be printed!")
    fasta = sequence_db[['taxid', 'index', 'sequence']].apply(lambda x: convert_to_fasta(x['taxid'], x['index'], x['sequence']), axis=1).to_list()
    with open(product + '.fasta', 'w') as f:
        f.write('\n'.join(fasta))
    sequence_db['index_name'] = sequence_db.apply(lambda x: "{0}_{1}".format(x['taxid'], x['index']), axis=1)
    print("printing to " + product + '.abundance.txt')
    sequence_db[['index_name', 'abundance']].to_csv(product + '.abundance.txt', sep='\t', header=None, index=None)


if __name__ == "__main__":
    simulate_metranscriptomic_abundances_inhost()