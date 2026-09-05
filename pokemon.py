from dataclasses import dataclass

@dataclass
class Pokemon:
    name: str
    id: int
    type: str
    height: float
    weight: float
    