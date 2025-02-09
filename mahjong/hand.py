from typing import List

import numpy as np

from .tile import Tile


class Hand:
    def __init__(self, tiles: List[Tile] = None):
        self.tiles = tiles
        if tiles is None:
            self.tiles = []

    def draw(self, tile: Tile):
        self.tiles.append(tile)

    def discard(self, tile: Tile):
        self.tiles.remove(tile)

    def count(self, tile: Tile):
        return self.tiles.count(tile)

    def mask(self) -> np.ndarray:
        data = [int(self.tiles.count(Tile(i)) > 0) for i in range(34)]
        return np.asarray(data, dtype=np.int8)

    def observation(self) -> np.ndarray:
        mask = np.asarray([self.tiles.count(Tile(i)) for i in range(34)])
        observation = []
        for i in range(4):
            observation.append(np.where(mask > i, 1, 0))
        return np.asarray(observation, dtype=np.int8)

    def __len__(self):
        return len(self.tiles)

    def __getitem__(self, item):
        return self.tiles[item]

    def __iter__(self):
        return iter(self.tiles)

    def __next__(self):
        return next(self.__iter__())
