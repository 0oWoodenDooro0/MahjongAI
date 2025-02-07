from abc import ABC, abstractmethod
from typing import Tuple

from .tile import Tile


class Meld(ABC):
    def __init__(self, tiles: Tuple[Tile, Tile, Tile] | Tuple[Tile, Tile, Tile, Tile]):
        if not self.is_valid(tiles):
            raise ValueError("Invalid tiles of Meld")
        self.tiles = tiles

    def __iter__(self):
        return iter(self.tiles)

    @staticmethod
    @abstractmethod
    def is_valid(tiles: Tuple[Tile, Tile, Tile] | Tuple[Tile, Tile, Tile, Tile]) -> bool:
        pass

    def __next__(self):
        return next(self.__iter__())


class TripletMeld(Meld):
    def __init__(self, tiles: Tuple[Tile, Tile, Tile]):
        super().__init__(tiles)

    @staticmethod
    def is_valid(tiles: Tuple[Tile, Tile, Tile]) -> bool:
        return tiles.count(tiles[0]) == 3


class SequenceMeld(Meld):
    def __init__(self, tiles: Tuple[Tile, Tile, Tile]):
        super().__init__(tiles)

    @staticmethod
    def is_valid(tiles: Tuple[Tile, Tile, Tile]) -> bool:
        min_tile = min(tiles)
        if min_tile >= Tile.W1:
            return False
        elif (min_tile + 1 not in tiles) or (min_tile + 2 not in tiles):
            return False
        elif (min_tile % 9 + 1 != (min_tile + 1) % 9) or (min_tile % 9 + 2 != (min_tile + 2) % 9):
            return False
        return True


class QuadrupletMeld(Meld):
    def __init__(self, tiles: Tuple[Tile, Tile, Tile, Tile]):
        super().__init__(tiles)

    @staticmethod
    def is_valid(tiles: Tuple[Tile, Tile, Tile, Tile]) -> bool:
        return tiles.count(tiles[0]) == 4
