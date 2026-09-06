from dataclasses import dataclass, field
from typing import List

from pokemon import Pokemon


@dataclass
class PokemonTeam:
    limit: int = 6
    team: List[Pokemon] = field(default_factory=list) # prevents instances of classes share same list
    size: int = 0


