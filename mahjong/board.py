import random
from typing import Optional

from .tile import Tile


class Board:
    def __init__(self):
        self.river: list[Tile] = []
        self.wall: list[Tile] = []
        for tile in Tile:
            self.wall.extend((tile, tile, tile, tile))
        random.shuffle(self.wall)

    def draw(self) -> Optional[Tile]:
        if len(self.wall) <= 16:
            return None
        return self.wall.pop()

    def discard_to_river(self, tile: Tile):
        self.river.append(tile)

    def get_last_discard_tile(self) -> Tile:
        return self.river.pop()
