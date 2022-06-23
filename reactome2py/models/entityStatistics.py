from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List

from .statistics import Statistics


@dataclass_json
@dataclass
class EntityStatistics(Statistics):
    curatedTotal: int
    curatedFound: int

    interactorsTotal: int
    interactorsFound: int

    pValue: float
    fdr: float
    exp: List[float]
