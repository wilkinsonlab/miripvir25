import pandas as pd
from scipy import stats
import numpy as np


def mann_whitney_posthoc(df: pd.DataFrame, factor_column, value_column):
    """
    Performs Mann-Whitney U tests between all pairs of groups in a dataset.
    This function conducts pairwise Mann-Whitney U tests (also known as Wilcoxon rank-sum test) 
    between all unique combinations of groups defined in the factor column. It's useful for 
    post-hoc analysis after finding significant differences in a Kruskal-Wallis test.
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the data to analyze
    factor_column : str
        Name of the column containing the grouping factor
    value_column : str
        Name of the column containing the numeric values to compare
    Returns
    -------
    pd.DataFrame
        DataFrame containing the results of all pairwise comparisons with columns:
        - group_1: First group in the comparison
        - group_2: Second group in the comparison 
        - U: Mann-Whitney U statistic
        - p-val: p-value of the test
        - sign: Boolean indicating if the difference is significant (p < 0.05)
    Notes
    -----
    The test is two-sided by default. For each pair, the groups are arranged so that
    the one with the higher mean is always first.
    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'habitat': ['A', 'A', 'B', 'B', 'C', 'C'],
    ...     'values': [1, 2, 3, 4, 5, 6]
    ... })
    >>> mann_whitney_posthoc(df, 'habitat', 'values')    

    """

    factors = df[factor_column].unique()
    out = []
    for h1, h2 in [(x, y) for x in factors for y in factors if x != y]:
        x = df.query(f'{factor_column} == "{h1}"')[value_column].values
        y = df.query(f'{factor_column} == "{h2}"')[value_column].values
        if x.mean() < y.mean():  # type: ignore
            x, y = y, x
        stat, pval = stats.mannwhitneyu(x, y, alternative='two-sided')
        
        out.append({
            'group_1': h1,
            'group_2': h2,
            'U': stat,
            'p-val': pval,
            'sign': pval < 0.05
        })
    df_out = pd.DataFrame.from_records(out)
    return df_out

def _randomize_regression(x: np.ndarray, y: np.ndarray):
    x_ = np.random.permutation(x)
    y_ = np.random.permutation(y)
    return x_, y_

def _regression(x, y):
    """
    Docstring for regression
    
    :param x: Description
    :param y: Description
    """
    u = stats.linregress(x, y) 
    return u.slope # type: ignore

def randomized_regression_test(x, y, repetitions=1000):
    """
    Docstring for randomized_regression_test
    
    
    """
    observed_slope = _regression(x, y)
    null_slope = np.stack([_regression(*_randomize_regression(x, y)) for _ in range(repetitions)])
    p_value = np.sum(_regression(x, y) < observed_slope) / len(null_slope)
    return {
        "observed_slope": observed_slope, 
        "null_slopes": null_slope, 
        "p-value": p_value
    }