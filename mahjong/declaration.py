from typing import List

from .meld import Meld, Tile, QuadrupletMeld, TripletMeld


class Declaration:
    def __init__(self, tiles: List[Meld] = None):
        self.tiles: List[Meld] = tiles
        if self.tiles is None:
            self.tiles = []

    def call(self, meld: Meld):
        self.tiles.append(meld)

    def add_kong(self, tile: Tile):
        for index in range(len(self.tiles)):
            if TripletMeld.is_valid(self.tiles[index].tiles):
                self.tiles[index] = QuadrupletMeld((tile, tile, tile, tile))

    def __get__(self, instance, owner):
        return self.tiles

    def __len__(self):
        return len(self.tiles)

    def __getitem__(self, index: int):
        return self.tiles[index]

    def __setitem__(self, index: int, value: Meld):
        self.tiles[index] = value

    def __iter__(self):
        return iter(self.tiles)

    def __next__(self):
        return next(self.__iter__())
