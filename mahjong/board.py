import random

from .tile import Tile


class Board:
    def __init__(self):
        self.river: list[Tile] = []
        self.wall: list[Tile] = []
        for tile in Tile:
            self.wall.extend((tile, tile, tile, tile))
        random.shuffle(self.wall)

    def draw(self) -> Tile:
        return self.wall.pop()

    def discard_to_river(self, tile: Tile):
        self.river.append(tile)
