
from dataclasses import dataclass, field
from .color import Color

@dataclass
class Event:
    id: int = -1
    name: str = ""
    desc: str = ""
    cancel: bool = False

    # Start et end son en UNIX TIME c'est à dire en secondes à partir de 1/1/1970 UTC, transformable en temps lisible par un humain via ce code:
    """
    from datetime import datetime

    user = User(start=1714233600)  # Exemple de timestamp UNIX
    dt = datetime.fromtimestamp(user.start)

    print(dt)  # format lisible : 2025-04-28 00:00:00
    """
    start: int = 0
    end: int = 0
    color: Color = field(default_factory=lambda: Color(255, 0, 0))
