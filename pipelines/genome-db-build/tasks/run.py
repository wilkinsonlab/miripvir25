import pandas as pd
import requests

def obtain_report_from_taxid(taxid):
    u = requests.get(f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{taxid}/dataset_report")
    u.raise_for_status()
    u = u.json()
    try:
        u = pd.DataFrame.from_records([dict(accession=item['accession'], organism=item['organism']['organism_name'], length=item['assembly_stats']['total_sequence_length']) for item in u['reports']]).sort_values(by='length', ascending=False).reset_index()
    except KeyError:
        return dict(taxid=taxid, organism=None, length=None)
    return dict(taxid=taxid, accesion=u.loc[0, 'accession'], organism=u.loc[0, 'organism'], length=u.loc[0, 'length'])

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
    return dict(taxid=taxid, accesion=accession, organism=organism, length=length)

def extract_sequence_ids(file):
    """
        
    """
    with open(file, 'r') as f:
        all_ids = list(filter(lambda x: x[0] == '>', f.readlines()))
        all_ids = [id.split(' ')[0].replace('>', '') for id in all_ids]
    return all_ids


def obtain_genome_accessions(product, reference_file):
    data = pd.read_csv(reference_file, header=None, names=['taxid'])
    reports = list(map(obtain_report_from_taxid, data['taxid'].unique().tolist()))
    reports = pd.DataFrame.from_records(reports)
    reports['length'] = reports['length'].astype(float)
    reports.dropna(subset='accesion').to_csv(product['genome_accessions'], sep="\t", index=None, header=None)

def obtain_accessions_taxid(product, reference_file):
    data = pd.read_csv(reference_file, header=None, names=['genome_accessions'])
    reports = list(map(obtain_report_from_accession, data['genome_accessions'].unique().tolist()))
    reports = pd.DataFrame.from_records(reports)
    reports['length'] = reports['length'].astype(float)
    reports.dropna(subset='accesion').to_csv(product['genome_accessions'], sep="\t", index=None, header=None)


def create_lookup_table(upstream, product, path):
    success = upstream['download']['success']
    success = pd.read_csv(success, header=None, names=['accession']).copy()
    out = []
    for _, row in success.iterrows():
        ids = extract_sequence_ids(path + '/' + row.accession + '.fna')
        out += [dict(accession=row.accession, sequence_id=seqid) for seqid in ids]
    pd.DataFrame.from_records(out).to_json(product['sequence_index'], indent=4, orient='records')
