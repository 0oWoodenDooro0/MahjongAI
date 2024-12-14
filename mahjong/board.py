import random

from .player import Player
from .tile import Tile

class Board:
    def __init__(self):
        self.river: list[Tile] = []
        self.wall: list[Tile] = []
        for tile in Tile:
            if tile in [Tile.Spring, Tile.Summer, Tile.Autumn, Tile.Winter,
                        Tile.Plum, Tile.Orchid, Tile.Bamboo, Tile.Chrysanth]:
                self.wall.append(tile)
            else:
                self.wall.extend((tile, tile, tile, tile))
        random.shuffle(self.wall)

    def deal(self, player: Player):
        tile = self.wall.pop()
        player.draw(tile)

    def discard_to_river(self, tile: Tile):
        self.river.append(tile)
