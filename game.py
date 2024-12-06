from board import Board
from player import Player


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(), Player(), Player(), Player()]

    def deal(self):
        for _ in range(16):
            for player in self.players:
                self.board.deal(player)
