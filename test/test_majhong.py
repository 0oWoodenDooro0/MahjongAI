from unittest import TestCase
from majhong import check_is_chow, check_is_kong, check_is_pong, check_is_win
from tile import Tile


class TestMajhong(TestCase):
    def test_deal(self):
        tile_chow_list1, tile_chow1 = [Tile.C3, Tile.C2], Tile.C1
        tile_chow_list2, tile_chow2 = [Tile.C3, Tile.C1], Tile.C2
        tile_chow_list3, tile_chow3 = [Tile.C7, Tile.C8], Tile.C9
        tile_chow_list4, tile_chow4 = [Tile.C9, Tile.C8], Tile.C8

        self.assertTrue(check_is_chow(tile_chow_list1, tile_chow1))
        self.assertTrue(check_is_chow(tile_chow_list2, tile_chow2))
        self.assertTrue(check_is_chow(tile_chow_list3, tile_chow3))
        self.assertTrue(check_is_chow(tile_chow_list4, tile_chow4))

        tile_kong_list, tile_kong = [Tile.D3, Tile.D3, Tile.D3], Tile.D3
        tile_pong_list, tile_pong = [Tile.D3, Tile.D3], Tile.D3
        self.assertTrue(check_is_pong(tile_pong_list, tile_pong))
        self.assertTrue(check_is_kong(tile_pong_list, tile_pong))
        self.assertFalse(check_is_pong(tile_kong_list, tile_kong))
        self.assertTrue(check_is_pong(tile_kong_list, tile_kong))
