from .declaration import Declaration
from .hand import Hand
from .meld import Meld, SequenceMeld, TripletMeld, QuadrupletMeld
from .tile import Tile


class Player:
    def __init__(self, turn: int):
        self.turn: int = turn
        self.hand: Hand = Hand()
        self.declaration: Declaration = Declaration()

    def draw(self, tile: Tile):
        self.hand.draw(tile)

    def discard(self, tile: Tile):
        if tile not in self.hand:
            raise ValueError("tile not in hand")
        self.hand.discard(tile)

    def add_to_declaration(self, meld: Meld):
        for tile in meld:
            self.discard(tile)
        self.declaration.call(meld)

    def chow(self, chow_tiles: SequenceMeld, discard_tile: Tile):
        self.hand.draw(discard_tile)
        self.add_to_declaration(chow_tiles)

    def pong(self, pong_tiles: TripletMeld, discard_tile: Tile):
        self.hand.draw(discard_tile)
        self.add_to_declaration(pong_tiles)

    def kong(self, kong_tiles: QuadrupletMeld, discard_tile: Tile):
        self.hand.draw(discard_tile)
        self.add_to_declaration(kong_tiles)

    def closed_kong(self, closed_kong_tiles: QuadrupletMeld):
        self.add_to_declaration(closed_kong_tiles)

    def add_kong(self, add_kong_tile: Tile):
        self.discard(add_kong_tile)
        self.declaration.add_kong(add_kong_tile)

    def __str__(self):
        return f"Player {self.turn}"
