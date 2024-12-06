from unittest import TestCase

from player import Player
from tile import Tile


class TestPlayer(TestCase):
    def test_player(self):
        player = Player()
        player.draw(Tile.C1)
        hand = player.hand
        self.assertEqual(hand[0], Tile.C1)
