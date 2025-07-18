import pandas as pd
import numpy as np

def create_random_interactions(n_nodes_a: int, n_nodes_b: int, n_interactions: int) -> pd.DataFrame:
    """
    Only aimed at debug purposes.
    """
    out = []

    for i in range(n_interactions):
        out.append({
            "a": np.random.randint(0, n_nodes_a, size=1)[0],
            "b": np.random.randint(0, n_nodes_b, size=1)[0]
        })

    return pd.DataFrame(out)



def randomize_interactions(df: pd.DataFrame, p: str, q: str, seed:int=42)->pd.DataFrame:
    """
    Creates an interactions table where interactions have been
    randomized. Useful to test the signficance of networ
    features. 

    Args:
        df: network interactions
        p: column name for the start of each edge
        q: column name for the end of each edge
        seed:

    Returns:
        A dataframe where interactions have been shuffled.

    """
    
    try:
        _ = df[p]
        _ = df[q]
    except KeyError:
        raise IOError(f"either {p} or {q} are missing on the dataframe")


    else:
        p_shuf = df.sample(frac=1.0, replace=False, random_state=seed).reset_index()[p].to_list()
        q_shuf = df.sample(frac=1.0, replace=False, random_state=seed + 1).reset_index()[q].to_list()
        
        return pd.DataFrame.from_dict({p: p_shuf, q: q_shuf})