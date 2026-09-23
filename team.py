from dataclasses import dataclass, field
from typing import List

from pokemon import Pokemon


@dataclass
class PokemonTeam:
    limit: int = 6
    team: List[Pokemon] = field(default_factory=list) # prevents instances of classes share same list

    def __getitem__(self, index: int) -> Pokemon:
        return self.team[index]

    @property
    def size(self) -> int:
        return len(self.team)

    def add_pokemon(self, pokemon: Pokemon) -> bool:
        if self.size >= self.limit:
            return False

        self.team.append(pokemon)
        return True

    def remove_pokemon(self, position: int) -> Pokemon | None:
        if position < 1 or position > self.size:
            return None
        return self.team.pop(position - 1)

