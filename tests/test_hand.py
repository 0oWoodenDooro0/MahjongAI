from unittest import TestCase

import numpy as np

from mahjong import Player, Tile, Hand


class TestHand(TestCase):
    def test_draw(self):
        hand = Hand()
        hand.draw(Tile.C1)
        self.assertEqual([Tile.C1], hand.tiles)

    def test_discard(self):
        hand = Hand([Tile.C1, Tile.C2, Tile.C3])
        hand.discard(Tile.C3)
        self.assertEqual([Tile.C1, Tile.C2], hand.tiles)

    def test_count(self):
        hand = Hand([Tile.C1, Tile.C2, Tile.C2])
        self.assertEqual(2, hand.count(Tile.C2))

    def test_mask(self):
        hand = Hand()
        hand.draw(Tile.C1)
        hand.draw(Tile.C2)
        mask = hand.mask()
        for i in range(34):
            if i == 0 or i == 1:
                self.assertEqual(1, mask[i])
            else:
                self.assertEqual(0, mask[i])

    def test_observation(self):
        hand = Hand()
        hand.draw(Tile.C1)
        hand.draw(Tile.C2)
        observation = hand.observation()
        np.testing.assert_equal(np.asarray([np.asarray(
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                            np.zeros(34), np.zeros(34), np.zeros(34)]), observation)
