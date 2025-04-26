
from dataclasses import dataclass

@dataclass
class Event:
    id: int = -1
    name: str = ""
    cancel: bool = False
