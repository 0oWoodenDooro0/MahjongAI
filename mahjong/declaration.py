from typing import List

import numpy as np

from .meld import Meld, Tile, QuadrupletMeld, TripletMeld


class Declaration:
    def __init__(self, melds: List[Meld] = None):
        self.melds: List[Meld] = melds
        if self.melds is None:
            self.melds = []

    def call(self, meld: Meld):
        self.melds.append(meld)

    def add_kong(self, tile: Tile):
        for index in range(len(self.melds)):
            if isinstance(self.melds[index], TripletMeld):
                if self.melds[index].tiles[0] == tile:
                    self.melds[index] = QuadrupletMeld((tile, tile, tile, tile))
                    return

    def observation(self):
        tiles = []
        for meld in self.melds:
            tiles.extend(list(meld.tiles))
        mask = np.asarray([tiles.count(Tile(i)) for i in range(34)])
        observation = []
        for i in range(4):
            observation.append(np.where(mask > i, 1, 0))
        return np.asarray(observation, dtype=np.int8)

    def __get__(self, instance, owner):
        return self.melds

    def __len__(self):
        return len(self.melds)

    def __getitem__(self, index: int):
        return self.melds[index]

    def __setitem__(self, index: int, value: Meld):
        self.melds[index] = value

    def __iter__(self):
        return iter(self.melds)

    def __next__(self):
        return next(self.__iter__())
