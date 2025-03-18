from unittest import TestCase

import numpy as np

from mahjong import Declaration, Tile, TripletMeld, SequenceMeld


class TestDeclaration(TestCase):
    def test_call(self):
        declaration = Declaration()
        declaration.call((TripletMeld((Tile.C9, Tile.C9, Tile.C9))))
        self.assertEqual((Tile.C9, Tile.C9, Tile.C9), declaration.melds[0].melds)

    def test_add_kong(self):
        declaration = Declaration()
        declaration.call(TripletMeld((Tile.C9, Tile.C9, Tile.C9)))
        declaration.add_kong(Tile.C9)
        self.assertEqual((Tile.C9, Tile.C9, Tile.C9, Tile.C9), declaration.melds[0].melds)

    def test_observation(self):
        declaration = Declaration()
        declaration.call(TripletMeld((Tile.C9, Tile.C9, Tile.C9)))
        np.testing.assert_equal(np.asarray([np.asarray(
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            np.asarray(
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.asarray(
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            np.zeros(34)]), declaration.observation())
