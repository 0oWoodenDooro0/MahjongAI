from board import Board
from player import Player
from tile import Tile

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(), Player(), Player(), Player()]

    def deal(self):
        for _ in range(16):
            for player in self.players:
                self.board.deal(player)

    def discard(self, player: Player, tile: Tile):
        player.discard(tile)
        self.board.discard_to_river(tile)

    def chou(self, player: Player, tile: Tile):
        player.chou(tile)

    def pong(self, player: Player, tile: Tile):
        player.pong(tile)

    def kong(self, player: Player, tile: Tile):
        player.kong(tile)
