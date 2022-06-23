from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Statistics:
    resource: str
    total: int
    found: int
    ratio: float
