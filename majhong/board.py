import random

from player import Player
from tile import Tile


class Board:
    def __init__(self):
        self.river: list[Tile] = []
        self.wall: list[Tile] = []
        for i in (tile.value for tile in Tile):
            self.wall.extend((Tile(i), Tile(i), Tile(i), Tile(i)))
        random.shuffle(self.wall)

    def deal(self, player: Player):
        tile = self.wall.pop()
        player.draw(tile)

    def discard_to_river(self, tile: Tile):
        pass
