from unittest import TestCase
from mahjong import Tile
from mahjong import (
    check_is_chow,
    check_is_kong,
    check_is_pong,
    check_is_win,
    check_listen,
)


class TestMahjong(TestCase):
    def test_check_is_chow(self):
        tile_chow_list1 = [Tile.C3, Tile.C2]
        tile_chow_list2 = [Tile.C3, Tile.C1]
        tile_chow_list3 = [Tile.C7, Tile.C8]
        tile_chow_list4 = [Tile.C9, Tile.C7]

        self.assertTrue(check_is_chow(tile_chow_list1, Tile.C1))
        self.assertTrue(check_is_chow(tile_chow_list2, Tile.C2))
        self.assertTrue(check_is_chow(tile_chow_list3, Tile.C9))
        self.assertTrue(check_is_chow(tile_chow_list4, Tile.C8))

    def test_check_is_kong(self):
        self.assertTrue(check_is_kong([Tile.D3, Tile.D3, Tile.D3], Tile.D3))
        self.assertFalse(check_is_kong([Tile.D3, Tile.D2, Tile.D3], Tile.D3))

    def test_check_is_pong(self):
        self.assertTrue(check_is_pong([Tile.D3, Tile.D3], Tile.D3))
        self.assertTrue(check_is_pong([Tile.D3, Tile.D3, Tile.D3], Tile.D3))
        self.assertFalse(check_is_pong([Tile.D3, Tile.D2], Tile.D3))

    def test_check_is_win(self):
        tile_win_list1 = [Tile.D3, Tile.D3, Tile.C7, Tile.C7]
        tile_win_list2 = [
            Tile.D3,
            Tile.D3,
            Tile.D3,
            Tile.C7,
            Tile.C7,
            Tile.C8,
            Tile.C8,
            Tile.B7,
            Tile.B7,
            Tile.B7,
        ]
        tile_win_list3 = [
            Tile.D1,
            # Tile.D2,
            Tile.D3,
            Tile.C4,
            Tile.C4,
            Tile.C4,
            Tile.B1,
            Tile.B1,
        ]
        self.assertTrue(check_is_win(tile_win_list1, Tile.C7))
        self.assertFalse(check_is_win(tile_win_list1, Tile.W1))

        self.assertTrue(check_is_win(tile_win_list2, Tile.C8))
        self.assertTrue(check_is_win(tile_win_list2, Tile.C7))
        self.assertFalse(check_is_win(tile_win_list2, Tile.B7))
        self.assertFalse(check_is_win(tile_win_list2, Tile.W1))

        self.assertTrue(check_is_win(tile_win_list3, Tile.D2))
        self.assertFalse(check_is_win(tile_win_list3, Tile.W1))

    def test_check_listen(self):
        tile1 = [
            Tile.C2,
            Tile.C2,
            Tile.C3,
            Tile.C6,
            Tile.C7,
            Tile.B1,
            Tile.B3,
            Tile.B8,
            Tile.B9,
            Tile.D3,
            Tile.D7,
            Tile.D8,
            Tile.W2,
            Tile.Dragon1,
            Tile.Dragon1,
            Tile.Dragon1,
        ]
        tile2 = [
            Tile.C1,
            Tile.C2,
            Tile.C3,
            Tile.C5,
            Tile.C6,
            Tile.C8,
            Tile.C9,
            Tile.B2,
            Tile.B3,
            Tile.B5,
            Tile.B6,
            Tile.B8,
            Tile.B9,
            Tile.D1,
            Tile.D2,
            Tile.D3,
        ]
        tile3 = [
            Tile.C1,
            Tile.C2,
            Tile.C3,
            Tile.C5,
            Tile.C6,
            Tile.C8,
            Tile.C9,
            Tile.B2,
            Tile.B3,
            Tile.B5,
            Tile.B6,
            Tile.B9,
            Tile.B9,
            Tile.D1,
            Tile.D2,
            Tile.D3,
        ]
        self.assertEqual(check_listen(tile1), 3)
        self.assertEqual(check_listen(tile2), 3)
        self.assertEqual(check_listen(tile3), 2)
