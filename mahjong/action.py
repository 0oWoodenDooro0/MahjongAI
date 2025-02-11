from enum import Enum, auto


class Action(Enum):
    DISCARD = auto()
    CHOW = auto()
    PONG = auto()
    KONG = auto()
    CLOSEDKONG = auto()
    ADDKONG = auto()
    WIN = auto()
