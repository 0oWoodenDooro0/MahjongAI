from unittest import TestCase
from majhong import check_is_chow, check_is_kong, check_is_pong, check_is_win
from tile import Tile


class TestMajhong(TestCase):
    def test_deal(self):
        tile_chow_list1 = [Tile.C3, Tile.C2]
        tile_chow_list2 = [Tile.C3, Tile.C1]
        tile_chow_list3 = [Tile.C7, Tile.C8]
        tile_chow_list4 = [Tile.C9, Tile.C7]

        self.assertTrue(check_is_chow(tile_chow_list1, Tile.C1))
        self.assertTrue(check_is_chow(tile_chow_list2, Tile.C2))
        self.assertTrue(check_is_chow(tile_chow_list3, Tile.C9))
        self.assertTrue(check_is_chow(tile_chow_list4, Tile.C8))

        tile_kong_list = [Tile.D3, Tile.D3, Tile.D3]
        tile_pong_list = [Tile.D3, Tile.D3]
        self.assertFalse(check_is_kong(tile_pong_list, Tile.D3))
        self.assertTrue(check_is_kong(tile_kong_list, Tile.D3))

        self.assertTrue(check_is_pong(tile_pong_list, Tile.D3))
        self.assertTrue(check_is_pong(tile_kong_list, Tile.D3))
        self.assertFalse(check_is_pong([Tile.D3, Tile.D2], Tile.D3))

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
