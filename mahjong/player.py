from .tile import Tile


class Player:
    def __init__(self):
        self.hand: list[Tile] = []
        self.decalaration: list[Tile] = []

    def draw(self, tile: Tile):
        self.hand.append(tile)

    def discard(self, tile: list[Tile]):
        self.hand.remove(tile)

    def chou(self, tile: list[Tile]):
        self.hand.remove(tile)
        self.decalaration.append(tile)

    def pong(self, tile: list[Tile]):
        self.hand.remove(tile)
        self.decalaration.append(tile)

    def kong(self, tile: list[Tile]):
        self.hand.remove(tile)
        self.decalaration.append(tile)
