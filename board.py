import random

from player import Player
from tile import Tile


class Board:
    def __init__(self):
        self.stack: list[Tile] = []
        for i in (tile.value for tile in Tile):
            self.stack.extend((Tile(i), Tile(i), Tile(i), Tile(i)))
        random.shuffle(self.stack)

    def deal(self, player: Player):
        tile = self.stack.pop()
        player.draw(tile)
