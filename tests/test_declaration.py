from unittest import TestCase

from mahjong import Declaration, Tile, TripletMeld, SequenceMeld


class TestDeclaration(TestCase):
    def test_call(self):
        declaration = Declaration()
        declaration.call((TripletMeld((Tile.C9, Tile.C9, Tile.C9))))
        self.assertEqual((Tile.C9, Tile.C9, Tile.C9), declaration.tiles[0].tiles)

    def test_add_kong(self):
        declaration = Declaration()
        declaration.call(TripletMeld((Tile.C9, Tile.C9, Tile.C9)))
        declaration.add_kong(Tile.C9)
        self.assertEqual((Tile.C9, Tile.C9, Tile.C9, Tile.C9), declaration.tiles[0].tiles)
