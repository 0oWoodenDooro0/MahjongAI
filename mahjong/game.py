from .board import Board
from .player import Player
from .tile import Tile


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(), Player(), Player(), Player()]

    def deal(self):
        for _ in range(16):
            for player in self.players:
                self.board.deal(player)

    def discard(self, player: Player, tile: Tile):
        pass

    def chou(self, player: Player, tile: Tile):
        pass

    def pong(self, player: Player, tile: Tile):
        pass

    def kong(self, player: Player, tile: Tile):
        pass
