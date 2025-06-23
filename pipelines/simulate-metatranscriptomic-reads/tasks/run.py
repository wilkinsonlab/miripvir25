import pandas as pd
import requests
from Bio import SeqIO
import numpy as np

def obtain_report_from_taxid(taxid):
    u = requests.get(f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{taxid}/dataset_report")
    u.raise_for_status()
    u = u.json()
    try:
        # u = pd.DataFrame.from_records([dict(accession=item['accession'], organism=item['organism']['organism_name'], length=item['assembly_stats']['total_sequence_length']) for item in u['reports']]).sort_values(by='length', ascending=False).reset_index()
        u = pd.DataFrame.from_records([dict(accession=item['accession'], organism=item['organism']['organism_name'], length=item['assembly_stats']['total_sequence_length']) for item in u['reports']])
    except KeyError:
        return dict(taxid=taxid, organism=None, length=None)
    return dict(taxid=taxid, accession=u.loc[0, 'accession'], organism=u.loc[0, 'organism'], length=u.loc[0, 'length'])

def obtain_report_from_accession(accession):
    u = requests.get(f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/{accession}/dataset_report")
    u.raise_for_status()
    u = u.json()
    try:
        taxid = str(u['reports'][0]['organism']['tax_id'])
        organism = u['reports'][0]['organism']['organism_name']
        length = u['reports'][0]['assembly_stats']['total_sequence_length']
    except KeyError:
        return dict(taxid=pd.NA, accession=accession, organism=pd.NA, length=None)
    except IndexError:
        return dict(taxid=pd.NA, accession=accession, organism=pd.NA, length=None)
    return dict(taxid=taxid, accession=accession, organism=organism, length=length)

def extract_sequences(file):
    """
        
    """
    with open(file, 'r') as f:
        sequences = SeqIO.parse(f, format='fasta')
        sequences = [dict(id=item.id, sequence=str(item.seq)) for item in sequences]
    return sequences



def obtain_genome_accessions(product, reference_file):
    data = pd.read_csv(reference_file, header=None, names=['taxid'])
    reports = list(map(obtain_report_from_taxid, data['taxid'].unique().tolist()))
    reports = pd.DataFrame.from_records(reports)
    reports['length'] = reports['length'].astype(float)
    reports[['taxid', 'accession', 'organism', 'length']].dropna(subset='accession').drop_duplicates(subset=['accession']).to_csv(product['genome_accessions'], sep="\t", index=None, header=None)

def obtain_accessions_taxid(product, reference_file):
    data = pd.read_csv(reference_file, header=None, names=['genome_accessions'])
    reports = list(map(obtain_report_from_accession, data['genome_accessions'].unique().tolist()))
    reports = pd.DataFrame.from_records(reports)
    reports['length'] = reports['length'].astype(float)
    reports[['taxid', 'accession', 'organism', 'length']].dropna(subset='accession').to_csv(product['genome_accessions'], sep="\t", index=None, header=None)


def catalogue(upstream, product, path):
    success = upstream['download']['success']
    success = pd.read_csv(success, header=None, names=['accession']).copy()

    accessions = upstream['accessions']['genome_accessions']
    accessions = pd.read_csv(accessions, sep='\t', header=None, names=['taxid', 'accession', 'organism', 'length'])
    out = []
    for i, row in success.iterrows():
        sequences = extract_sequences(path + '/' + row.accession + '.cds.fna')
        out += [dict(accession=row.accession, index='f{:06d}'.format(j), sequence_id=seq['id'], sequence=seq['sequence'], sequence_length=len(seq['sequence'])) for j, seq in enumerate(sequences)]
    out = pd.DataFrame.from_records(out)
    pd.merge(out, accessions, on='accession').to_json(product['sequence_index'], indent=4, orient='records')


def simulate_abundance(product, db, host_taxon_id, host_abundance, other_species_sample_mean, other_species_sample_sigma):
    others_abundance = 1 - host_abundance
    sequence_db = pd.read_json(db)
    sequence_db['weight'] = sequence_db['sequence_length'] / sequence_db['length']


    host = sequence_db[sequence_db.taxid == host_taxon_id].copy()
    others = sequence_db[sequence_db.taxid != host_taxon_id].copy()

    host['abundance'] = host['weight'] * host_abundance

    others_s = others[['taxid']].drop_duplicates('taxid')
    others_s['r'] = np.random.lognormal(
        mean=other_species_sample_mean, 
        sigma=other_species_sample_sigma, 
        size=len(others_s)
    )
    others_s['r'] = others_s['r'] / others_s['r'].sum()

    others = pd.merge(others, others_s, on='taxid')
    others['abundance'] = others['r'] * others['weight'] * others_abundance

    sampling_df = pd.concat((host[['taxid', 'index', 'abundance', 'sequence']], others[['taxid', 'index', 'abundance', 'sequence']]))
    sampling_df['abundance'] = sampling_df['abundance'] / sampling_df['abundance'].sum()
    fasta = sampling_df[['taxid', 'index', 'sequence']].apply(lambda x: convert_to_fasta(x['taxid'], x['index'], x['sequence']), axis=1).to_list()
    with open(product['fasta'], 'w') as f:
        f.write('\n'.join(fasta))

    sampling_df['index_name'] = sampling_df.apply(lambda x: "{0}_{1}".format(x['taxid'], x['index']), axis=1)
    sampling_df[['index_name', 'abundance']].to_csv(product['abundances'], sep='\t', header=None, index=None)


def simulate_lognormal_data(x, mean, sigma):
    y = np.random.lognormal(
        mean=mean, 
        sigma=sigma, 
        size=x 
    )
    return y / y.sum()

def simulate_metatranscriptomic_abundance(product, db, host_taxon_id, host_abundance, other_species_sample_mean, other_species_sample_sigma):
    others_abundance = 1 - host_abundance
    sequence_db = pd.read_json(db)
    sequence_db['weight'] = sequence_db.groupby('taxid')['sequence_length'].transform(lambda x: x / x.sum())
    sequence_db['s'] = sequence_db.groupby(['taxid'], as_index=False).apply(lambda x: simulate_lognormal_data(len(x), 0.5, 2.0)).explode().values

    host = sequence_db[sequence_db.taxid == host_taxon_id].copy()
    host['abundance'] = (host['weight'] * host['s'] / (host['weight'] * host['s']).sum()) * host_abundance

    others = sequence_db[sequence_db.taxid != host_taxon_id].copy()
    others_s = others[['taxid']].drop_duplicates('taxid')
    others_s['r'] = np.random.lognormal(
        mean=other_species_sample_mean, 
        sigma=other_species_sample_sigma, 
        size=len(others_s)
    )
    others_s['r'] = others_s['r'] / others_s['r'].sum()
    others = pd.merge(others, others_s, on='taxid')
    others['abundance'] = others['r'] * others['weight'] * others['s'] 
    others['abundance'] = others_abundance * others['abundance'] / others['abundance'].sum()

    sampling_df = pd.concat((host[['taxid', 'index', 'abundance', 'sequence']], others[['taxid', 'index', 'abundance', 'sequence']]))
    sampling_df['abundance'] = sampling_df['abundance'] / sampling_df['abundance'].sum()
    fasta = sampling_df[['taxid', 'index', 'sequence']].apply(lambda x: convert_to_fasta(x['taxid'], x['index'], x['sequence']), axis=1).to_list()
    with open(product['fasta'], 'w') as f:
        f.write('\n'.join(fasta))

    sampling_df['index_name'] = sampling_df.apply(lambda x: "{0}_{1}".format(x['taxid'], x['index']), axis=1)
    sampling_df[['index_name', 'abundance']].to_csv(product['abundances'], sep='\t', header=None, index=None)

def convert_to_fasta(taxid, index, sequence):
    return f">{taxid}_{index}\n{sequence}"
