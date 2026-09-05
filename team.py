from dataclasses import dataclass
from typing import List

from pokemon import Pokemon


@dataclass
class PokemonTeam:
    limit: int
    team: List[Pokemon]


