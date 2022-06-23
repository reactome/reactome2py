from __future__ import annotations

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional

from .entityStatistics import EntityStatistics
from .reactionStatistics import ReactionStatistics


@dataclass_json
@dataclass
class EventHierarchyNode:
    stId: str
    name: str
    species: str
    type: str
    diagram: bool
    url: Optional[str] = None
    entities: Optional[EntityStatistics] = None
    reactions: Optional[ReactionStatistics] = None
    children: Optional[List[EventHierarchyNode]] = None
