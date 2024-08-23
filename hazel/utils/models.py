from dataclasses import dataclass
from enum import Enum


class Root(Enum):
    SOFTWARE = "software hacker"
    PITCH = "pitch competition hacker"


class Leaf(Enum):
    GAMING = "gaming theme"
    SECURITY = "security theme"
    FINANCE = "finance theme"
    SOCIAL = "social impact theme"


class Branch(Enum):
    AI = "ai track"
    BLOCKCHAIN = "blockchain track"
    DATA = "data visualization track"


@dataclass
class Hacker:
    username: str
    root: Root
    leaf: Leaf
    branch: Branch
