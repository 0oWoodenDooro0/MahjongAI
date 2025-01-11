from typing import List, Tuple

import numpy as np

from .tile import Tile


class Player:
    def __init__(self, turn: int):
        self.turn = turn
        self.hand: List[Tile] = []
        self.declaration: List[Tuple[Tile, Tile, Tile] | Tuple[Tile, Tile, Tile, Tile]] = []

    def add_to_hand(self, tile: Tile):
        self.hand.append(tile)

    def discard(self, tile: Tile):
        if tile not in self.hand:
            raise ValueError("tile not in hand")
        self.hand.remove(tile)

    def add_to_declaration(self, tiles: Tuple[Tile, Tile, Tile] | Tuple[Tile, Tile, Tile, Tile]):
        for tile in tiles:
            self.discard(tile)
        self.declaration.append(tiles)

    def chow(self, chow_tiles: Tuple[Tile, Tile, Tile], discard_tile: Tile):
        self.hand.append(discard_tile)
        self.add_to_declaration(chow_tiles)

    def pong(self, pong_tiles: Tuple[Tile, Tile, Tile], discard_tile: Tile):
        self.hand.append(discard_tile)
        self.add_to_declaration(pong_tiles)

    def kong(self, kong_tiles: Tuple[Tile, Tile, Tile, Tile], discard_tile: Tile):
        self.hand.append(discard_tile)
        self.add_to_declaration(kong_tiles)

    def closed_kong(self, closed_kong_tiles: Tuple[Tile, Tile, Tile, Tile]):
        self.add_to_declaration(closed_kong_tiles)

    def add_kong(self, add_kong_tile: Tile):
        self.discard(add_kong_tile)
        for index in range(len(self.declaration)):
            if self.declaration[index] == (add_kong_tile, add_kong_tile, add_kong_tile):
                self.declaration[index] = (add_kong_tile, add_kong_tile, add_kong_tile, add_kong_tile)

    def get_mask(self):
        data = list(int(self.hand.count(Tile(i)) > 0) for i in range(34))
        return np.asarray(data, dtype=np.int8)

    def __str__(self):
        return f"Player {self.turn}"
