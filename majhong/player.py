from tile import Tile


class Player:
    def __init__(self):
        self.hand: list[Tile] = []
        self.decalaration: list[Tile] = []

    def draw(self, tile: Tile):
        self.hand.append(tile)

    def discard(self, tile: Tile):
        pass

    def chou(self, tile: Tile):
        pass

    def pong(self, tile: Tile):
        pass

    def kong(self, tile: Tile):
        pass

    def claim_to_declaration(self):
        pass