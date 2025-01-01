from typing import Optional

from .action import Action
from .board import Board
from .player import Player
from .tile import Tile
from .util import check_is_self_win, check_is_win, check_is_kong, check_is_pong, check_is_chow, check_is_add_kong, \
    check_is_closed_kong


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(0), Player(1), Player(2), Player(3)]
        self.turn = 0
        self.over = False
        self.next_step = []

    def init_game(self):
        self.deal()
        draw_tile = self.draw()
        self.get_turn_player().add_to_hand(draw_tile)
        self.next_step = self.check_draw_next_step()
        infos = self.next_step[0]
        observations = self.get_observation()
        return observations, infos

    def deal(self):
        for _ in range(16):
            for player in self.players:
                draw_tile = self.board.draw()
                player.add_to_hand(draw_tile)

    def draw(self) -> Optional[Tile]:
        draw_tile = self.board.draw()
        print(f"draw {draw_tile} left {len(self.board.wall)}")
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
        player = self.get_turn_player()
        print(f"{player} chow {chow_tiles}!")
        player.add_to_hand(self.get_discard_tile())
        for tile in chow_tiles:
            player.discard(tile)
        player.add_to_declaration(chow_tiles)

    def pong(self, pong_tiles: tuple[Tile, Tile, Tile]):
        player = self.get_turn_player()
        print(f"{player} pong {pong_tiles}!")
        player.add_to_hand(self.get_discard_tile())
        for tile in pong_tiles:
            player.discard(tile)
        player.add_to_declaration(pong_tiles)

    def kong(self, kong_tiles: tuple[Tile, Tile, Tile, Tile]):
        player = self.get_turn_player()
        print(f"{player} kong {kong_tiles}!")
        player.add_to_hand(self.get_discard_tile())
        for tile in kong_tiles:
            player.discard(tile)
        player.add_to_declaration(kong_tiles)
        player.add_to_hand(self.draw())

    def win(self):
        print(f"{self.get_turn_player()} wins!")
        self.over = True

    def add_kong(self, add_kong_tile: Tile):
        player = self.get_turn_player()
        print(f"{player} add kong!")
        player.add_kong(add_kong_tile)
        player.add_to_hand(self.draw())

    def closed_kong(self, draw_tile: Tile, closed_kong_tiles: tuple[Tile, Tile, Tile, Tile]):
        player = self.get_turn_player()
        print(f"{player} closed kong!")
        player.add_to_hand(draw_tile)
        for tile in closed_kong_tiles:
            player.discard(tile)
        player.add_to_declaration(closed_kong_tiles)
        player.add_to_hand(self.draw())

    def discard(self, discard_tile: Tile):
        player = self.get_turn_player()
        print(f"{player} discard {discard_tile}!")
        player.discard(discard_tile)
        self.board.discard_to_river(discard_tile)
        print(self.board.river)

    def check_discard_next_step(self, discard_tile: Tile):
        next_step = []
        for player in self.players:
            if player.turn == self.turn:
                continue
            elif check_is_win(player.hand, discard_tile):
                next_step.append({"win": {"player": player.turn, "tile": None}})
        for player in self.players:
            if player.turn == self.turn:
                continue
            if kong_tiles := check_is_kong(player.hand, discard_tile):
                next_step.append({"kong": {"player": player.turn, "tile": kong_tiles, "type": "kong"}})
            if pong_tiles := check_is_pong(player.hand, discard_tile):
                next_step.append({"pong": {"player": player.turn, "tile": pong_tiles}})
        for player in self.players:
            if player.turn == (self.turn + 1) % len(self.players):
                if chow_tiles_list := check_is_chow(player.declaration, discard_tile):
                    for chow_tiles in chow_tiles_list:
                        next_step.append({"chow": {"player": player.turn, "tile": chow_tiles}})
        return next_step

    def check_draw_next_step(self):
        next_step = []
        player = self.get_turn_player()
        if check_is_self_win(player.hand):
            next_step.append({"win": {"player": player.turn, "tile": None}})
        if add_kong_tile_list := check_is_add_kong(player.declaration, player.hand):
            for add_kong_tile in add_kong_tile_list:
                next_step.append({"kong": {"player": player.turn, "tile": (add_kong_tile,), "type": "add_kong"}})
        if closed_kong_tiles := check_is_closed_kong(player.hand):
            next_step.append({"kong": {"player": player.turn, "tile": closed_kong_tiles, "type": "closed_kong"}})
        if not next_step:
            next_step.append({"discard": {"player": player.turn, "tile": None, "mask": player.get_mask()}})
        return next_step

    def step(self, action: Action, turn: int, tiles: Optional[tuple[Tile]]):
        player = self.players[turn]
        rewards = {}
        infos = {}
        match action:
            case Action.DISCARD:
                self.discard(tiles[0])
                discard_tile = tiles[0]
                self.next_step = self.check_discard_next_step(discard_tile)
                self.turn_next()
            case Action.CHOW:
                self.turn = player.turn
                self.chow(tiles)
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.get_mask()}}]
            case Action.PONG:
                self.turn = player.turn
                self.pong(tiles)
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.get_mask()}}]
            case Action.KONG:
                self.turn = player.turn
                self.kong(tiles)
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.get_mask()}}]
            case Action.CLOSEDKONG:
                self.closed_kong(tiles[0], tiles)
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.get_mask()}}]
            case Action.ADDKONG:
                self.add_kong(tiles[0])
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.get_mask()}}]
            case Action.WIN:
                self.win()
            case Action.NOTHING:
                if self.next_step:
                    self.next_step.pop(0)

        if not self.next_step:
            draw_tile = self.draw()
            if draw_tile is None:
                return self.get_observation(), rewards, self.over, infos
            self.get_turn_player().add_to_hand(draw_tile)
            self.next_step = self.check_draw_next_step()
        infos = self.next_step[0]

        observations = self.get_observation()

        return observations, rewards, self.over, infos

    def get_observation(self):
        other = self.board.river
        for player in self.players:
            for declarartion in player.declaration:
                other.extend(declarartion)
        player = self.get_turn_player()
        return [player.hand.count(Tile(i)) for i in range(34)] + [other.count(Tile(i)) for i in range(34)]
