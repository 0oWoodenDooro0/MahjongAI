import numpy as np

from .tile import Tile


class Player:
    def __init__(self, turn: int):
        self.turn = turn
        self.hand: list[Tile] = []
        self.declaration: list[tuple[Tile, Tile, Tile] | tuple[Tile, Tile, Tile, Tile]] = []

    def add_to_hand(self, tile: Tile):
        self.hand.append(tile)

    def discard(self, tile: Tile):
        if tile not in self.hand:
            raise ValueError("tile not in hand")
        self.hand.remove(tile)

    def add_to_declaration(self, tiles: tuple[Tile, Tile, Tile] | tuple[Tile, Tile, Tile, Tile]):
        self.declaration.append(tiles)

    def add_kong(self, tile: Tile):
        for index in range(len(self.declaration)):
            if self.declaration[index] == (tile, tile, tile):
                self.declaration[index] = (tile, tile, tile, tile)

    def get_mask(self):
        data = list(int(self.hand.count(Tile(i)) > 0) for i in range(34))
        return np.asarray(data, dtype=np.int8)

    def __str__(self):
        return f"Player{self.turn}"
