from .tile import Tile


class Player:
    def __init__(self):
        self.hand: list[Tile] = []
        self.decalaration: list[Tile] = []

    def add_to_hand(self, tile: Tile):
        self.hand.append(tile)

    def discard(self, tile: Tile):
        self.hand.remove(tile)

    def add_to_decalaration(self, tile: Tile):
        self.decalaration.append(tile)
