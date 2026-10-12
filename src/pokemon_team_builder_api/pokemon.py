from dataclasses import dataclass, field

@dataclass
class Pokemon:
    name: str
    id: int
    types: list[str]
    height: float
    weight: float
    base_stats: dict[str, int]
    weaknesses: list[str] = field(default_factory=list)

