from copy import deepcopy
from typing import List
from collections import Counter

import numpy as np

from .meld import Meld
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

    def claim_observation(self, meld: Meld) -> np.ndarray:
        tiles = deepcopy(self.tiles)
        for tile in meld:
            if tile in tiles:
                tiles.remove(tile)
        mask = np.asarray([tiles.count(Tile(i)) for i in range(34)])
        observation = []
        for i in range(4):
            observation.append(np.where(mask > i, 1, 0))
        return np.asarray(observation, dtype=np.int8)

    def observation(self) -> np.ndarray:
        mask = np.asarray([self.tiles.count(Tile(i)) for i in range(34)])
        observation = []
        for i in range(4):
            observation.append(np.where(mask > i, 1, 0))
        return np.asarray(observation, dtype=np.int8)

    def check_listen_count(self) -> int:
        def _count_combos_and_partners(tiles: List[Tile]) -> List[int]:
            if len(tiles) == 0:
                return [0, 0]

            result: List[int]  # return (面子，搭子)
            min_tile = min(tiles)
            sub_tiles = tiles.copy()

            if tiles.count(min_tile) >= 3:
                for _ in range(3):
                    sub_tiles.remove(min_tile)
                result = _count_combos_and_partners(sub_tiles)
                result[0] += 1
                return result

            if ((next := min_tile.next_seq_tile(1)) not in tiles) or (
                    min_tile.next_seq_tile(2) not in tiles
            ):
                sub_tiles.remove(min_tile)
                if tiles.count(min_tile) == 2:
                    sub_tiles.remove(min_tile)
                elif next in tiles:
                    sub_tiles.remove(next)
                elif (next_2 := min_tile.next_seq_tile(2)) in tiles:
                    sub_tiles.remove(next_2)
                else:
                    return _count_combos_and_partners(sub_tiles)
                result = _count_combos_and_partners(sub_tiles)
                result[1] += 1
                return result

            sub_tiles.remove(min_tile)
            sub_tiles.remove(min_tile.next_seq_tile(1))
            sub_tiles.remove(min_tile.next_seq_tile(2))
            result = _count_combos_and_partners(sub_tiles)
            result[0] += 1
            return result

        # ---------------------------------------------------------
        # reference from https://www.bilibili.com/opus/563332111030452322

        pairs: List = [i for i, c in Counter(self.tiles).items() if c >= 2]
        has_pair: bool = len(pairs) > 0

        result: List[int] = _count_combos_and_partners(self.tiles)
        combos: int = result[0]
        partners: int = result[1]
        combos += (16 - len(self.tiles)) // 3

        if combos + partners <= 6:
            return 10 - 2 * combos - partners
        else:
            return 5 - combos - has_pair

    @property
    def listen_count(self) -> int:
        return self.check_listen_count()

    def __len__(self):
        return len(self.tiles)

    def __getitem__(self, item):
        return self.tiles[item]

    def __iter__(self):
        return iter(self.tiles)

    def __next__(self):
        return next(self.__iter__())
