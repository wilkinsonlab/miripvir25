import pandas as pd
from miripvir.data import BlastPairedEndReads, LookUpTable, Hits
from difflib import SequenceMatcher
import logging
from typing import List
import random


def blast_filter(
    reads: BlastPairedEndReads, library_name: str, query_coverage: int, length_threshold: int, 
    lookup_table: LookUpTable, remove_prefix=False
) -> Hits:
    """
    Applies a protocol for filtering BLAST hits similar to what
    was implemented in McLeish2024. See the Notes section for more details.

    Args:
        reads: Sequencing reads (forward and backward) mapped by BLAST in table format.
        library_name: Name of the library, needed to output files.
        query_coverage: Percentage of the query that should be spanned by the mapped fragments.
        length_threshold: Length of the mapped sequence.
        lookup_table: Table connecting the IDs of the mapping sequences with the accession and taxids

    Returns:
        Filtered and grouped hits


    Notes:

        This command enables a complex pipeline with different steps. These ones
        are bundled together in this script to ease testing.
        1. Remove mapped sequences with lengths under length_threshold
        2. Remove mapped sequences with query coverages under query_coverage
        3. Remove sequences whose paired ends did not align to the same reference sequences
        4. Remove sequences whose alignment is ambiguous (e.g. mapping to two different locations)
        5. Group all results by species hits


    """
    source_1 = reads.source_1
    source_2 = reads.source_2
    reads_1 = remove_prefixes(reads.reads_1, remove_prefix=remove_prefix, randomize=True)
    reads_2 = remove_prefixes(reads.reads_2, remove_prefix=remove_prefix, randomize=True)
    reads = pd.concat([reads_1, reads_2])
    
    original_length = len(reads)
    # STEP 1 - Mapping criteria
    logging.debug(f"original file size: {len(reads)}")
    reads = blast_filter_by_length(reads, length_threshold)
    logging.debug(f"after filter by length>={length_threshold}, size: {len(reads)}")
    reads = blast_filter_by_qcoverage(reads, query_coverage)
    logging.debug(f"after filter by qcovs>={query_coverage}, size: {len(reads)}")
    # STEP 2 - Paired ends
    # best_reads['base_id'] = best_reads['read'].apply(lambda x: x.replace("J00148:56:HM5WHBBXX:1:", "").replace("J00148:56:HM5WHBBXX:2:", ""))
    reads = blast_filter_paired_end(reads)
    logging.debug(f"after filter by paired ends, size: {len(reads)}")
    # STEP 3 - Remove ambiguous mappings
    reads = blast_filter_ambiguous(reads)
    logging.debug(f"after filter by ambiguity, size: {len(reads)}")
    # STEP 4 - Group and report by species
    hits = blast_display_results_by_OTUs(reads, lookup_table.reference)
    hits['library'] = library_name
    
    hits = Hits(
        hits=hits, query_coverage=query_coverage,
        length_threshold=length_threshold, reference=lookup_table.source,
        original_length=original_length, final_length=len(reads),
        source_1=source_1, source_2=source_2
    )
    return hits
    


def blast_filter_by_length(df: pd.DataFrame, length_threshold: int) -> pd.DataFrame:
    """
    Removes mappings with lengths under a length_theshold

    Args:
        df: Input data
        length_threshold: length value

    Returns:
        Table where all mappings should be above the threshold
    """
    return df.query(f'length >= {length_threshold}').copy()

def blast_filter_by_qcoverage(df: pd.DataFrame, query_coverage: int) -> pd.DataFrame:
    """
    Removes mappings with query_coverages under a query_coverage threshold

    Args:
        df: Input data
        query_coverage: query coverage value

    Returns:
        Table where all mappings should be above the threshold
    """
    return df.query(f'qcovs >= {query_coverage}').copy()

def blast_filter_paired_end(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes mappings whose paired end query sequence did not align against 
    to the same reference sequence

    Args:
        df: Input data

            
    Returns:
        Table with forward mappings whose backward sequence mapped the same reference sequence
    """
    paired = df.groupby(['base_id', 'ref'], as_index=False)['file'].nunique()
    paired = paired[paired.file == 2]
    df = df[df['base_id'].isin(paired['base_id'])].query('file == "forward"')
    return df

def blast_filter_ambiguous(df:pd.DataFrame) -> pd.DataFrame:
    """
    Removes mappings that either map to different reference sequences
    or map to the same reference at different locations.

    Args:
        df: Input data
        lookup_table: Reference data

    Returns:
        Table without ambiguous mappings
    """
    # TODO: Move this to the function where we read the files.
    df['ref'] = df['ref'].apply(
        lambda x: x.replace(
            "ref|", ''
        ).replace(
            'gb|', ''
        ).replace(
            'emb|', ''
        ).replace(
            'dbj|', ''
        ).replace(
            'tpe|', ''
        ).replace(
            '|', ''
        ))
    unambiguous = df.value_counts(subset=['base_id', 'ref']).reset_index().value_counts(subset=['base_id']).reset_index().query('count < 2')
    return df[df.base_id.isin(unambiguous.base_id)].copy()
    
def blast_display_results_by_OTUs(df: pd.DataFrame, lookup_table: pd.DataFrame):
    """
    Creates a table with value counts per organism.

    Args:
        df: Input data
        

    Returns:
        Table without ambiguous mappings
    """
    df = pd.merge(df, lookup_table, left_on='ref', right_on='sequence_id', how='left')
    return df.value_counts(subset=['taxid', 'organism']).reset_index()

def find_substring_match(x:List[str], randomize=False, samples=1000) -> str:
    """
    Finds the minimal common substring in a list of strings

    Args:
        x: Input data
        random: whether to use the deterministic algorithm or not.
        samples: number of iterations        

    Returns:
        Minimal common substring


    """
    minimal_match = "X"*1000
    if randomize:
        x = x.copy()
        random.shuffle(x)

    for i, x1 in enumerate(x[1:samples]):
        for j, x2 in enumerate(x[:i + 1]):
            match = SequenceMatcher(None, x1, x2).find_longest_match()
            if match.size < len(minimal_match):
                minimal_match = x2[match.a:match.a + match.size]
    return minimal_match

def remove_prefixes(df: pd.DataFrame, remove_prefix=True, randomize=True):
    """
    Removes prefix out of reads. 

    Args:
        df: Input data
        
    Returns:
        Table where the ´read´ parameter should not contain a prefix
    """
    if remove_prefix:
        example = find_substring_match(df['read'].unique().tolist(), randomize=randomize)
        df['base_id'] = df['read'].apply(lambda x: x.replace(example, ''))
    else:
        df['base_id'] = df['read']
    return df

