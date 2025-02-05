from unittest import TestCase

from mahjong import Player, Tile, SequenceMeld, TripletMeld, QuadrupletMeld, Hand, Declaration


class TestPlayer(TestCase):
    def test_add_to_hand(self):
        player = Player(0)
        player.draw(Tile.C1)
        hand = player.hand
        self.assertEqual(Tile.C1, hand[0])

    def test_discard(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.discard(Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertRaises(ValueError, player.discard, Tile.C2)

    def test_add_to_declaration(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C2)
        player.draw(Tile.C3)
        player.add_to_declaration(SequenceMeld((Tile.C1, Tile.C2, Tile.C3)))
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0].tiles)

    def test_chow(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C3)
        player.chow(SequenceMeld((Tile.C1, Tile.C2, Tile.C3)), Tile.C2)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0].tiles)

    def test_pong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.pong(TripletMeld((Tile.C1, Tile.C1, Tile.C1)), Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_kong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.kong(QuadrupletMeld((Tile.C1, Tile.C1, Tile.C1, Tile.C1)), Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_closed_kong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.closed_kong(QuadrupletMeld((Tile.C1, Tile.C1, Tile.C1, Tile.C1)))
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_add_kong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.pong(TripletMeld((Tile.C1, Tile.C1, Tile.C1)), Tile.C1)
        player.draw(Tile.C1)
        player.add_kong(Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_can_chow(self):
        player = Player(0)
        player.hand = Hand([Tile.C3, Tile.C2])
        result1 = player.can_chow(Tile.C1)
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), result1[0].tiles)
        player.hand = Hand([Tile.C3, Tile.C1])
        result2 = player.can_chow(Tile.C2)
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), result2[0].tiles)
        player.hand = Hand([Tile.C7, Tile.C8])
        result3 = player.can_chow(Tile.C9)
        self.assertEqual((Tile.C7, Tile.C8, Tile.C9), result3[0].tiles)
        player.hand = Hand([Tile.C9, Tile.C7])
        result4 = player.can_chow(Tile.C8)
        self.assertEqual((Tile.C7, Tile.C8, Tile.C9), result4[0].tiles)
        player.hand = Hand([Tile.B9, Tile.C7])
        result5 = player.can_chow(Tile.C8)
        self.assertIsNone(result5)
        player.hand = Hand([Tile.C2, Tile.C3, Tile.C4, Tile.C5, Tile.C6])
        result6 = player.can_chow(Tile.C4)
        self.assertEqual((Tile.C2, Tile.C3, Tile.C4), result6[0].tiles)
        self.assertEqual((Tile.C3, Tile.C4, Tile.C5), result6[1].tiles)
        player.hand = Hand([Tile.W2, Tile.W3])
        result7 = player.can_chow(Tile.W1)
        self.assertEqual((Tile.C4, Tile.C5, Tile.C6), result6[2].tiles)
        self.assertIsNone(result7)

    def test_can_pong(self):
        player = Player(0)
        player.hand = Hand([Tile.D3, Tile.D3])
        self.assertEqual((Tile.D3, Tile.D3, Tile.D3), player.can_pong(Tile.D3).tiles)
        player.hand = Hand([Tile.D3, Tile.D3, Tile.D3])
        self.assertEqual((Tile.D3, Tile.D3, Tile.D3), player.can_pong(Tile.D3).tiles)
        player.hand = Hand([Tile.D3, Tile.D2])
        self.assertIsNone(player.can_pong(Tile.D3))

    def test_can_kong(self):
        player = Player(0)
        player.hand = Hand([Tile.D3, Tile.D3, Tile.D3])
        self.assertEqual((Tile.D3, Tile.D3, Tile.D3, Tile.D3), player.can_kong(Tile.D3).tiles)
        player.hand = Hand([Tile.D3, Tile.D2, Tile.D3])
        self.assertIsNone(player.can_kong(Tile.D3))

    def test_can_closed_kong(self):
        player = Player(0)
        player.hand = Hand([Tile.D3, Tile.D3, Tile.D3, Tile.D3])
        self.assertEqual((Tile.D3, Tile.D3, Tile.D3, Tile.D3), player.can_closed_kong().tiles)
        player.hand = Hand([Tile.D3, Tile.D2, Tile.D3, Tile.D3])
        self.assertIsNone(player.can_closed_kong())

    def test_can_add_kong(self):
        player = Player(0)
        player.hand = Hand([Tile.D3])
        player.declaration = Declaration(
            [SequenceMeld((Tile.C1, Tile.C2, Tile.C3)), TripletMeld((Tile.D3, Tile.D3, Tile.D3))])
        self.assertEqual(Tile.D3, player.can_add_kong()[0])
        player.hand = Hand([Tile.D3])
        player.declaration = Declaration([SequenceMeld((Tile.C1, Tile.C2, Tile.C3))])
        self.assertIsNone(player.can_add_kong())

    def test_can_win(self):
        player = Player(0)
        player.hand = Hand([Tile.D3, Tile.D3, Tile.C7, Tile.C7])
        self.assertTrue(player.can_win(Tile.C7))
        self.assertFalse(player.can_win(Tile.W1))
        player.hand = Hand([Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.B7, Tile.B7, Tile.B7])
        self.assertTrue(player.can_win(Tile.C8))
        self.assertTrue(player.can_win(Tile.C7))
        self.assertFalse(player.can_win(Tile.B7))
        self.assertFalse(player.can_win(Tile.W1))
        player.hand = Hand([Tile.D1, Tile.D3, Tile.C4, Tile.C4, Tile.C4, Tile.B1, Tile.B1])
        self.assertTrue(player.can_win(Tile.D2))
        self.assertFalse(player.can_win(Tile.W1))
        player.hand = Hand([Tile.W1, Tile.W1, Tile.W2, Tile.W3, Tile.W4, Tile.Dragon2])
        self.assertFalse(player.can_win(Tile.Dragon3))
        player.hand = Hand([Tile.C8, Tile.C9, Tile.D1, Tile.B7, Tile.B7, Tile.B7])
        self.assertFalse(player.can_win(Tile.D2))

    def test_can_self_win(self):
        player = Player(0)
        player.hand = Hand([Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C7])
        self.assertTrue(player.can_self_win())
        player.hand = Hand([Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.W1])
        self.assertFalse(player.can_self_win())
        player.hand = Hand(
            [Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.B7, Tile.B7, Tile.B7, Tile.C8])
        self.assertTrue(player.can_self_win())
        player.hand = Hand(
            [Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.B7, Tile.B7, Tile.B7, Tile.C7])
        self.assertTrue(player.can_self_win())
        player.hand = Hand(
            [Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.B7, Tile.B7, Tile.B7, Tile.B7])
        self.assertFalse(player.can_self_win())
        player.hand = Hand(
            [Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.B7, Tile.B7, Tile.B7, Tile.W1])
        self.assertFalse(player.can_self_win())
        player.hand = Hand([Tile.D1, Tile.D3, Tile.C4, Tile.C4, Tile.C4, Tile.B1, Tile.B1, Tile.D2])
        self.assertTrue(player.can_self_win())
        player.hand = Hand([Tile.D1, Tile.D3, Tile.C4, Tile.C4, Tile.C4, Tile.B1, Tile.B1, Tile.W1])
        self.assertFalse(player.can_self_win())
        player.hand = Hand(
            [Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.D9, Tile.B1, Tile.B2, Tile.C7])
        self.assertFalse(player.can_self_win())
        player.hand = Hand(
            [Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.W3, Tile.W4, Tile.Dragon1, Tile.C7])
        self.assertFalse(player.can_self_win())

    def test_check_is_win(self):
        self.assertTrue(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B1]))
        self.assertTrue(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B2]))
        self.assertTrue(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B4]))
        self.assertTrue(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B5]))
        self.assertTrue(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B7]))
        self.assertTrue(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B8]))
        self.assertFalse(Player.check_is_win(
            [Tile.B2, Tile.B3, Tile.B3, Tile.B3, Tile.B3, Tile.B4, Tile.B5, Tile.B6, Tile.B6, Tile.B6, Tile.B6, Tile.B7,
             Tile.B8, Tile.B9]))

        self.assertFalse(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C1]))
        self.assertFalse(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C2]))
        self.assertFalse(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C3]))
        self.assertFalse(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C4]))
        self.assertTrue(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C5]))
        self.assertTrue(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C6]))
        self.assertTrue(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C8]))
        self.assertTrue(Player.check_is_win(
            [Tile.C1, Tile.C1, Tile.C1, Tile.C2, Tile.C2, Tile.C2, Tile.C6, Tile.C7, Tile.C7, Tile.C7, Tile.C7, Tile.C8,
             Tile.C9, Tile.C9]))

    def test_check_listen_count(self):
        player = Player(0)
        player.hand = Hand(
            [Tile.C2, Tile.C2, Tile.C3, Tile.C6, Tile.C7, Tile.B1, Tile.B3, Tile.B8, Tile.B9, Tile.D3, Tile.D7, Tile.D8,
             Tile.W2, Tile.Dragon1, Tile.Dragon1, Tile.Dragon1])
        self.assertEqual(player.check_listen_count(), 3)
        player.hand = Hand(
            [Tile.C1, Tile.C2, Tile.C3, Tile.C5, Tile.C6, Tile.C8, Tile.C9, Tile.B2, Tile.B3, Tile.B5, Tile.B6, Tile.B8,
             Tile.B9, Tile.D1, Tile.D2, Tile.D3])
        self.assertEqual(player.check_listen_count(), 3)
        player.hand = Hand(
            [Tile.C1, Tile.C2, Tile.C3, Tile.C5, Tile.C6, Tile.C8, Tile.C9, Tile.B2, Tile.B3, Tile.B5, Tile.B6, Tile.B9,
             Tile.B9, Tile.D1, Tile.D2, Tile.D3])
        self.assertEqual(player.check_listen_count(), 2)
        player.hand = Hand([Tile.D3, Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C8, Tile.C8, Tile.D9, Tile.B1, Tile.B2])
        self.assertEqual(player.check_listen_count(), 1)
