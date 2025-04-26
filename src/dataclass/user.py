
from dataclasses import dataclass

@dataclass
class User:
    id: int = -1
    mail: str = ""
    mdp: str = ""
