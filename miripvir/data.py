from pydantic.dataclasses import dataclass
from datetime import datetime
import pandas as pd

class GeneralConfig:
    arbitrary_types_allowed=True

@dataclass(config=GeneralConfig)
class BlastPairedEndReads:
    reads_1: pd.DataFrame
    reads_2: pd.DataFrame
    source_1: str
    source_2: str
@dataclass(config=GeneralConfig)
class LookUpTable:
    
    source: str
    reference: pd.DataFrame

@dataclass(config=GeneralConfig)
class Hits:
    
    hits: pd.DataFrame
    query_coverage: int
    length_threshold: int
    reference: str
    original_length: int
    final_length: int
    source_1: str
    source_2: str