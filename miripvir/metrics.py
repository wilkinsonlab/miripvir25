from typing import List

def assess_taxonomic_classification_metrics(reference: List[List[int]] , results: List[int], method: str):
    """
    Enables comparing the accuracy of a taxonomy classifier, even when
    the reference and the test used different taxonomic systems (which
    is an issue with GTDB classification)


    Args:
        reference: the reference classification
        results: the classification under benchmark
        method: just a label to add to the results

    Returns:
        Filtered and grouped hits


    Notes:
        1. This function counts true-positives (TP), false-negatives (FN), false-positives (FP), and the length of the reference and the result.
        2. A positive is given if a hit found in the results has at least one hit across all the terms in the test.
        3. False negatives are computed as the total of positives minus the true positives.
    """
    results = set(list(results)) # De-replication
    reference_flat = [item2 for item1 in reference for item2 in item1]
    true_positives = 0
    false_positives = 0

    true_positives = len(list(filter(lambda x: x in reference_flat, results)))
    false_positives = len(list(filter(lambda x: x not in reference_flat, results)))
    false_negatives = len(reference) - true_positives

    return dict(method=method, TP=true_positives, FP=false_positives, FN=false_negatives, P=len(results), Q=len(reference))