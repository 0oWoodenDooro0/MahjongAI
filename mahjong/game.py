from typing import Optional

from .board import Board
from .player import Player
from .tile import Tile


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(0), Player(1), Player(2), Player(3)]
        self.turn = 0
        self.over = False
        self.deal()

    def deal(self):
        for _ in range(16):
            for player in self.players:
                draw_tile = self.board.draw()
                player.add_to_hand(draw_tile)

    def draw(self) -> Optional[Tile]:
        draw_tile = self.board.draw()
        if draw_tile is None:
            self.over = True
        return draw_tile

    def get_discard_tile(self) -> Tile:
        return self.board.get_last_discard_tile()

    def get_turn_player(self) -> Player:
        return self.players[self.turn]

    def turn_next(self):
        self.turn = (self.turn + 1) % len(self.players)

    def chow(self, chow_tiles: tuple[Tile, Tile, Tile]):
        print(f"Player{self.turn} chow {chow_tiles}!")
        player = self.get_turn_player()
        player.add_to_hand(self.get_discard_tile())
        for tile in chow_tiles:
            player.discard(tile)
        player.add_to_declaration(chow_tiles)

    def pong(self, pong_tiles: tuple[Tile, Tile, Tile]):
        print(f"Player{self.turn} pong {pong_tiles}!")
        player = self.get_turn_player()
        player.add_to_hand(self.get_discard_tile())
        for tile in pong_tiles:
            player.discard(tile)
        player.add_to_declaration(pong_tiles)

    def kong(self, kong_tiles: tuple[Tile, Tile, Tile, Tile]):
        print(f"Player{self.turn} kong {kong_tiles}!")
        player = self.get_turn_player()
        player.add_to_hand(self.get_discard_tile())
        for tile in kong_tiles:
            player.discard(tile)
        player.add_to_declaration(kong_tiles)
        player.add_to_hand(self.board.draw())

    def win(self):
        print(f"Player{self.turn} wins!")
        self.over = True

    def add_kong(self, add_kong_tile: Tile):
        print(f"Player{self.turn} add kong!")
        player = self.get_turn_player()
        player.add_kong(add_kong_tile)
        player.add_to_hand(self.board.draw())

    def closed_kong(self, draw_tile: Tile, closed_kong_tiles: tuple[Tile, Tile, Tile, Tile]):
        print(f"Player{self.turn} closed kong!")
        player = self.get_turn_player()
        player.add_to_hand(draw_tile)
        for tile in closed_kong_tiles:
            player.discard(tile)
        player.add_to_declaration(closed_kong_tiles)
        player.add_to_hand(self.board.draw())

    def discard(self, discard_tile: Tile):
        print(f"Player{self.turn} discard {discard_tile}!")
        player = self.get_turn_player()
        player.discard(discard_tile)
        self.board.discard_to_river(discard_tile)
