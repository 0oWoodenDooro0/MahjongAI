from tile import Tile


class Player:
    def __init__(self):
        self.hand: list[Tile] = []

    def draw(self, tile: Tile):
        self.hand.append(tile)
