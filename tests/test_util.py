from unittest import TestCase

from mahjong import Tile
from mahjong import (
    check_is_chow,
    check_is_kong,
    check_is_closed_kong,
    check_is_add_kong,
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
        tile_chow_list5 = [Tile.B9, Tile.C7]
        tile_chow_list6 = [Tile.C2, Tile.C3, Tile.C4, Tile.C5, Tile.C6]
        tile_chow_list7 = [Tile.W2, Tile.W3]

        result1 = check_is_chow(tile_chow_list1, Tile.C1)
        result2 = check_is_chow(tile_chow_list2, Tile.C2)
        result3 = check_is_chow(tile_chow_list3, Tile.C9)
        result4 = check_is_chow(tile_chow_list4, Tile.C8)
        result5 = check_is_chow(tile_chow_list5, Tile.C8)
        result6 = check_is_chow(tile_chow_list6, Tile.C4)
        result7 = check_is_chow(tile_chow_list7, Tile.W1)
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), result1[0])
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), result2[0])
        self.assertEqual((Tile.C7, Tile.C8, Tile.C9), result3[0])
        self.assertEqual((Tile.C7, Tile.C8, Tile.C9), result4[0])
        self.assertIsNone(result5)
        self.assertEqual((Tile.C2, Tile.C3, Tile.C4), result6[0])
        self.assertEqual((Tile.C3, Tile.C4, Tile.C5), result6[1])
        self.assertEqual((Tile.C4, Tile.C5, Tile.C6), result6[2])
        self.assertIsNone(result7)

    def test_check_is_kong(self):
        self.assertEqual(
            (Tile.D3, Tile.D3, Tile.D3, Tile.D3),
            check_is_kong([Tile.D3, Tile.D3, Tile.D3], Tile.D3),
        )
        self.assertIsNone(check_is_kong([Tile.D3, Tile.D2, Tile.D3], Tile.D3))

    def test_check_is_closed_kong(self):
        self.assertEqual(
            (Tile.D3, Tile.D3, Tile.D3, Tile.D3),
            check_is_closed_kong([Tile.D3, Tile.D3, Tile.D3], Tile.D3),
        )
        self.assertIsNone(check_is_closed_kong([Tile.D3, Tile.D2, Tile.D3], Tile.D3))

    def test_check_is_add_kong(self):
        self.assertEqual(
            Tile.D3,
            check_is_add_kong(
                [(Tile.C1, Tile.C2, Tile.C3), (Tile.D3, Tile.D3, Tile.D3)], Tile.D3
            ),
        )
        self.assertIsNone(check_is_add_kong([(Tile.C1, Tile.C2, Tile.C3)], Tile.D3))

    def test_check_is_pong(self):
        self.assertEqual(
            (Tile.D3, Tile.D3, Tile.D3), check_is_pong([Tile.D3, Tile.D3], Tile.D3)
        )
        self.assertEqual(
            (Tile.D3, Tile.D3, Tile.D3),
            check_is_pong([Tile.D3, Tile.D3, Tile.D3], Tile.D3),
        )
        self.assertIsNone(check_is_pong([Tile.D3, Tile.D2], Tile.D3))

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
        tile_win_list4 = [
            Tile.W1,
            Tile.W1,
            Tile.W2,
            Tile.W3,
            Tile.W4,
            Tile.Dragon2,
            # Tile.Dragon3,
        ]
        tile_win_list5 = [
            Tile.C8,
            Tile.C9,
            Tile.D1,
            # Tile.D2,
            Tile.B7,
            Tile.B7,
            Tile.B7,
        ]

        self.assertTrue(check_is_win(tile_win_list1, Tile.C7))
        self.assertFalse(check_is_win(tile_win_list1, Tile.W1))

        self.assertTrue(check_is_win(tile_win_list2, Tile.C8))
        self.assertTrue(check_is_win(tile_win_list2, Tile.C7))
        self.assertFalse(check_is_win(tile_win_list2, Tile.B7))
        self.assertFalse(check_is_win(tile_win_list2, Tile.W1))

        self.assertTrue(check_is_win(tile_win_list3, Tile.D2))
        self.assertFalse(check_is_win(tile_win_list3, Tile.W1))
        self.assertFalse(check_is_win(tile_win_list4, Tile.Dragon3))
        self.assertFalse(check_is_win(tile_win_list5, Tile.D2))

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
        tile4 = [
            Tile.D3,
            Tile.D3,
            Tile.D3,
            Tile.C7,
            Tile.C7,
            Tile.C8,
            Tile.C8,
            Tile.D9,
            Tile.B1,
            Tile.B2,
        ]
        self.assertEqual(check_listen(tile1), 3)
        self.assertEqual(check_listen(tile2), 3)
        self.assertEqual(check_listen(tile3), 2)
        self.assertEqual(check_listen(tile4), 1)
