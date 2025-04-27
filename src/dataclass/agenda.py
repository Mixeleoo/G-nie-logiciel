
from dataclasses import dataclass, field
from .color import Color

@dataclass
class Agenda:
    id: int = -1
    name: str = ""
    color: Color = field(default_factory=lambda: Color(255, 0, 0))
