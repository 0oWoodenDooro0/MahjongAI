from unittest import TestCase

import numpy as np

from mahjong import Player, Tile, Hand, SequenceMeld


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

    def test_claim_observation(self):
        meld = SequenceMeld((Tile(1), Tile(2), Tile(3)))
        hand = Hand([Tile(1), Tile(2), Tile(3), Tile(4)])
        self.assertEqual([Tile(4)], hand.claim_observation(meld))

    def test_observation(self):
        hand = Hand()
        hand.draw(Tile.C1)
        hand.draw(Tile.C2)
        observation = hand.observation()
        np.testing.assert_equal(np.asarray([np.asarray(
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            np.zeros(34), np.zeros(34), np.zeros(34)]), observation)

    def test_check_listen_count(self):
        hand = Hand(
            [Tile.C2, Tile.C2, Tile.C3, Tile.C6, Tile.C7, Tile.B1, Tile.B3, Tile.B8, Tile.B9, Tile.D3, Tile.D7, Tile.D8,
             Tile.W2, Tile.Dragon1, Tile.Dragon1, Tile.Dragon1])
        self.assertEqual(hand.check_listen_count(), 3)
        hand = Hand(
            [Tile.C1, Tile.C2, Tile.C3, Tile.C5, Tile.C6, Tile.C8, Tile.C9, Tile.B2, Tile.B3, Tile.B5, Tile.B6, Tile.B8,
             Tile.B9, Tile.D1, Tile.D2, Tile.D3])
        self.assertEqual(hand.check_listen_count(), 3)
        hand = Hand(
            [Tile.C1, Tile.C2, Tile.C3, Tile.C5, Tile.C6, Tile.C8, Tile.C9, Tile.B2, Tile.B3, Tile.B5, Tile.B6, Tile.B9,
             Tile.B9, Tile.D1, Tile.D2, Tile.D3])
        self.assertEqual(hand.check_listen_count(), 2)
        hand = Hand([Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.D9, Tile.B1, Tile.B2])
        self.assertEqual(hand.check_listen_count(), 1)
        hand = Hand([Tile.C1, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.D9, Tile.B1, Tile.B2])
        self.assertEqual(hand.check_listen_count(), 1)
