from typing import Optional

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

    def init_game(self):
        self.deal()
        draw_tile = self.draw()
        self.get_turn_player().draw(draw_tile)
        self.next_step = self.check_draw_next_step()
        infos = self.next_step[0]
        observations = self.get_observations()
        return observations, infos

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
        rewards = {}
        infos = {}
        next_step = self.next_step[0]
        action_agent = list(next_step.keys())[0]
        next_action = next_step[action_agent]
        player = self.players[next_action["player"]]
        match next_action["type"]:
            case Action.DISCARD:
                discard_tile = Tile(action)
                player.discard(discard_tile)
                self.board.discard_to_river(discard_tile)
                self.next_step = self.check_discard_next_step(discard_tile)
                self.turn_next()
            case Action.CHOW:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.turn = player.turn
                    player.chow(next_action["tile"], self.get_discard_tile())
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
            case Action.PONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.turn = player.turn
                    player.pong(next_action["tile"], self.get_discard_tile())
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
            case Action.KONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.turn = player.turn
                    player.kong(next_action["tile"], self.get_discard_tile())
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
            case Action.CLOSEDKONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    player.closed_kong(next_action["tile"])
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
            case Action.ADDKONG:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    player.add_kong(next_action["tile"])
                    self.next_step = [{"discard": {"player": self.turn, "tile": None, "type": Action.DISCARD}}]
            case Action.WIN:
                if action == 0 and self.next_step:
                    self.next_step.pop(0)
                else:
                    self.win()

        if not self.next_step:
            draw_tile = self.draw()
            if draw_tile is None:
                return {}, rewards, {}, infos
            self.get_turn_player().draw(draw_tile)
            self.next_step = self.check_draw_next_step()
        next_step = self.next_step[0]
        action_agent = list(next_step.keys())[0]
        infos = self.next_step[0]

        observations = self.get_observations()

        return observations, rewards, {action_agent: False}, infos

    def get_observations(self) -> dict[str, dict[str, ndarray[int, dtype[int]] | ndarray | None]]:
        next_step = self.next_step[0]
        action_agent = list(next_step.keys())[0]
        next_action = next_step[action_agent]
        action_type = next_action["type"]
        self_player = self.players[next_action["player"]]
        observation = self_player.hand.observation()
        for player in self.players:
            if player.turn == self_player.turn:
                continue
            observation = np.concatenate((observation, player.declaration.observation()))
        observation = np.concatenate((observation, self.board.river_observation()))
        observations = {action_agent: {"observation": observation,
                                       "action_mask": self_player.hand.mask() if action_type == Action.DISCARD else None}}
        return observations
