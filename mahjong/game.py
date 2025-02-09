from typing import Optional, Any

import numpy as np
from numpy import ndarray, dtype

from .action import Action
from .board import Board
from .meld import SequenceMeld, TripletMeld, QuadrupletMeld, Meld
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
                next_step.append({"win": {"player": player.turn, "tile": None}})
        for player in self.players:
            if player.turn == self.turn:
                continue
            if kong_tiles := player.can_kong(discard_tile):
                next_step.append({"kong": {"player": player.turn, "tile": kong_tiles, "type": "kong"}})
            if pong_tiles := player.can_pong(discard_tile):
                next_step.append({"pong": {"player": player.turn, "tile": pong_tiles}})
        for player in self.players:
            if player.turn == (self.turn + 1) % len(self.players):
                if chow_tiles_list := player.can_chow(discard_tile):
                    for chow_tiles in chow_tiles_list:
                        next_step.append({"chow": {"player": player.turn, "tile": chow_tiles}})
        return next_step

    def check_draw_next_step(self):
        next_step = []
        player = self.get_turn_player()
        if player.can_self_win():
            next_step.append({"win": {"player": player.turn, "tile": None}})
        if add_kong_tile_list := player.can_add_kong():
            for add_kong_tile in add_kong_tile_list:
                next_step.append({"kong": {"player": player.turn, "tile": add_kong_tile, "type": "add_kong"}})
        if closed_kong_tiles := player.can_closed_kong():
            next_step.append({"kong": {"player": player.turn, "tile": closed_kong_tiles, "type": "closed_kong"}})
        if not next_step:
            next_step.append({"discard": {"player": player.turn, "tile": None}})
        return next_step

    def step(self, action: Action, turn: int, tiles: Optional[Meld] = None, tile: Optional[Tile] = None):
        player = self.players[turn]
        rewards = {}
        infos = {}
        match action:
            case Action.DISCARD:
                if not isinstance(tile, Tile):
                    raise AttributeError("not correct tile in discard")
                player.discard(tile)
                self.board.discard_to_river(tile)
                self.next_step = self.check_discard_next_step(tile)
                self.turn_next()
            case Action.CHOW:
                self.turn = player.turn
                if not isinstance(tiles, SequenceMeld):
                    raise AttributeError(tiles, "not correct tile in chow")
                player.chow(tiles, self.get_discard_tile())
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.hand.mask()}}]
            case Action.PONG:
                self.turn = player.turn
                if not isinstance(tiles, TripletMeld):
                    raise AttributeError(tiles, "not correct meld pong")
                player.pong(tiles, self.get_discard_tile())
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.hand.mask()}}]
            case Action.KONG:
                self.turn = player.turn
                if not isinstance(tiles, QuadrupletMeld):
                    raise AttributeError(tiles, "not correct meld in kong")
                player.kong(tiles, self.get_discard_tile())
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.hand.mask()}}]
            case Action.CLOSEDKONG:
                if not isinstance(tiles, QuadrupletMeld):
                    raise AttributeError(tiles, "not correct meld in closed kong")
                player.closed_kong(tiles)
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.hand.mask()}}]
            case Action.ADDKONG:
                if not isinstance(tile, Tile):
                    raise AttributeError(tile, "not correct tile in add kong")
                player.add_kong(tile)
                self.next_step = [{"discard": {"player": self.turn, "tile": None, "mask": player.hand.mask()}}]
            case Action.WIN:
                self.win()
            case Action.NOTHING:
                if self.next_step:
                    self.next_step.pop(0)

        if not self.next_step:
            draw_tile = self.draw()
            if draw_tile is None:
                return self.get_observations(), rewards, self.over, infos
            self.get_turn_player().draw(draw_tile)
            self.next_step = self.check_draw_next_step()
        infos = self.next_step[0]

        observations = self.get_observations()

        return observations, rewards, self.over, infos

    def get_observations(self) -> dict[str, ndarray[int, dtype[int]]]:
        self_player = self.get_turn_player()
        observation = self_player.hand.observation()
        for player in self.players:
            if player.turn == self_player.turn:
                continue
            observation = np.concatenate((observation, player.declaration.observation()))
        observation = np.concatenate((observation, self.board.river_observation()))
        observations = {
            "observation": observation,
            "mask": self_player.hand.mask()
        }
        return observations
