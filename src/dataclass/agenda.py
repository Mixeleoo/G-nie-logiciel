
from dataclasses import dataclass, field
from src.dataclass.color import Color

@dataclass
class Agenda:
    id: int = -1
    name: str = ""
    color: Color = field(default_factory=lambda: Color(255, 0, 0))
