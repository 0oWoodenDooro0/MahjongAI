from .tile import Tile


class Player:
    def __init__(self, turn: int):
        self.turn = turn
        self.hand: list[Tile] = []
        self.declaration: list[tuple[Tile, Tile, Tile] | tuple[Tile, Tile, Tile, Tile]] = []

    def add_to_hand(self, tile: Tile):
        self.hand.append(tile)

    def discard(self, tile: Tile):
        self.hand.remove(tile)

    def add_to_declaration(self, tiles: tuple[Tile, Tile, Tile] | tuple[Tile, Tile, Tile, Tile]):
        self.declaration.append(tiles)
