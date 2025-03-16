import copy
from typing import Optional, Dict, Any

import numpy as np
from numpy import ndarray, dtype

from .action import Action
from .board import Board
from .player import Player
from .tile import Tile


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(0), Player(1), Player(2), Player(3)]
        self.turn = 0
        self.over = False
        self.next_step = []
        self.state: Dict[str, Any] = {"move_count": 0, "win": None, "draw": None, "player": None, "action": None,
                                      "hand": None, "discard": None}

    def init_game(self):
        self.deal()
        draw_tile = self.draw()
        self.get_turn_player().draw(draw_tile)
        self.next_step = self.check_draw_next_step()

    def deal(self):
        for _ in range(16):
            for player in self.players:
                draw_tile = self.board.draw()
                player.draw(draw_tile)

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

    def win(self):
        self.over = True

    def check_discard_next_step(self, discard_tile: Tile):
        next_step = []
        for player in self.players:
            if player.turn == self.turn:
                continue
            elif player.can_win(discard_tile):
                next_step.append({"win": {"player": player.turn, "tile": None, "type": Action.WIN}})
        for player in self.players:
            if player.turn == self.turn:
                continue
            if kong_tiles := player.can_kong(discard_tile):
                next_step.append({"kong": {"player": player.turn, "tile": kong_tiles, "type": Action.KONG}})
            if pong_tiles := player.can_pong(discard_tile):
                next_step.append({"pong": {"player": player.turn, "tile": pong_tiles, "type": Action.PONG}})
        for player in self.players:
            if player.turn == (self.turn + 1) % len(self.players):
                if chow_tiles_list := player.can_chow(discard_tile):
                    for chow_tiles in chow_tiles_list:
                        next_step.append({"chow": {"player": player.turn, "tile": chow_tiles, "type": Action.CHOW}})
        return next_step

    def check_draw_next_step(self):
        next_step = []
        player = self.get_turn_player()
        if player.can_self_win():
            next_step.append({"win": {"player": player.turn, "tile": None, "type": Action.WIN}})
        if add_kong_tile_list := player.can_add_kong():
            for add_kong_tile in add_kong_tile_list:
                next_step.append({"kong": {"player": player.turn, "tile": add_kong_tile, "type": Action.ADDKONG}})
        if closed_kong_tiles := player.can_closed_kong():
            next_step.append({"kong": {"player": player.turn, "tile": closed_kong_tiles, "type": Action.CLOSEDKONG}})
        if not next_step:
            next_step.append({"discard": {"player": player.turn, "tile": None, "type": Action.DISCARD}})
        return next_step

    def step(self, action: int):
        self.state["draw"] = None
        self.state["discard"] = None
        next_step = self.next_step[0]
        action_agent = list(next_step.keys())[0]
        next_action = next_step[action_agent]
        player = self.players[next_action["player"]]
        self.state["player"] = str(player)
        self.state["action"] = next_action["type"]
        match next_action["type"]:
            case Action.DISCARD:
                discard_tile = Tile(action)
                player.discard(discard_tile)
                self.board.discard_to_river(discard_tile)
                self.next_step = self.check_discard_next_step(discard_tile)
                self.turn_next()
                self.state["move_count"] += 1
                self.state["discard"] = discard_tile
                if len(self.get_turn_player().hand.tiles) not in [1, 4, 7, 10, 13, 16]:
                    raise Exception("not right hand tiles")
            case Action.CHOW:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.turn = player.turn
                    player.chow(next_action["tile"], self.get_discard_tile())
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
                    self.state["move_count"] += 1
            case Action.PONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.turn = player.turn
                    player.pong(next_action["tile"], self.get_discard_tile())
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
                    self.state["move_count"] += 1
            case Action.KONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.turn = player.turn
                    player.kong(next_action["tile"], self.get_discard_tile())
                    player.draw(self.board.wall.pop(0))
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
                    self.state["move_count"] += 1
            case Action.CLOSEDKONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    player.closed_kong(next_action["tile"])
                    player.draw(self.board.wall.pop(0))
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
                    self.state["move_count"] += 1
            case Action.ADDKONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    player.add_kong(next_action["tile"])
                    player.draw(self.board.wall.pop(0))
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
                    self.state["move_count"] += 1
            case Action.WIN:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.win()
                    self.state["move_count"] += 1
                    self.state["win"] = True
                if len(self.get_turn_player().hand.tiles) not in [1, 4, 7, 10, 13, 16]:
                    raise Exception("not right hand tiles")

        if not self.next_step:
            draw_tile = self.draw()
            self.state["draw"] = draw_tile
            if draw_tile is None:
                self.over = True
                return
            self.get_turn_player().draw(draw_tile)
            self.next_step = self.check_draw_next_step()

        self.state["hand"] = sorted(copy.deepcopy(self.get_turn_player().hand.tiles))
