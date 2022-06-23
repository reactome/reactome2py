from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .statistics import Statistics


@dataclass_json
@dataclass
class ReactionStatistics(Statistics):
    pass
