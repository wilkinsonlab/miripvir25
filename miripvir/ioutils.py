import pandas as pd
from miripvir.data import BlastPairedEndReads, LookUpTable

def read_paired_end_files(file_forward: str, file_backward: str)->BlastPairedEndReads:
    """
    Reads a BLAST result applied to Illumina paired-end results.

    Args:
        file_forward: strand 1
        file_backward: strand 2
    Return:
        An object containing each of the reads and the files they come from.
    """
    read1 = pd.read_csv(file_forward, sep="\s+", header=None, names=['read', 'ref', 'identity', 'length', 'mismatch', 'gap', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore', 'qlen', 'qcovs'])
    read2 = pd.read_csv(file_backward, sep="\s+", header=None, names=['read', 'ref', 'identity', 'length', 'mismatch', 'gap', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore', 'qlen', 'qcovs'])
    read1['file'] = 'forward'
    read2['file'] = 'backward'
    bper = BlastPairedEndReads(
        reads_1=read1, reads_2=read2, source_1=str(file_forward), source_2=str(file_backward)
    )
    return bper

def read_blastdb_reference(reference: str)-> LookUpTable:
    """
    Returns a lookup table object from a BLAST DB lookup reference

    Args:
        reference: path to the json file working as reference

    Returns:
        An object containing all the data.

    """
    return LookUpTable(
        source=str(reference),
        reference=pd.read_json(reference)
    )