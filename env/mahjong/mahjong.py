import functools
from copy import deepcopy
from typing import Dict, Any

import numpy as np
from gymnasium import logger
from gymnasium.spaces import Discrete, MultiDiscrete
from numpy import ndarray, dtype
from pettingzoo.utils.env import ParallelEnv

import copy
from mahjong import Game, Action


def parallel_env(render_mode=None):
    return MahjongParallelEnv(render_mode=render_mode)


class MahjongParallelEnv(ParallelEnv):
    metadata = {"render_mode": ["human"], "name": "majhong_env_v0"}

    def __init__(self, render_mode=None):
        self.state = {}
        self.possible_agents = ["discard", "chow", "pong", "kong", "win"]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )
        self.render_mode = render_mode
        self.game = Game()
        self.state = self.game.state

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        observation_spaces = {
            "discard": MultiDiscrete([20, 34]),
            "chow": MultiDiscrete([8, 34]),
            "pong": MultiDiscrete([8, 34]),
            "kong": MultiDiscrete([8, 34]),
            "win": MultiDiscrete([4, 34]),
        }
        return observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        action_spaces = {
            "discard": Discrete(34),
            "chow": Discrete(2),
            "pong": Discrete(2),
            "kong": Discrete(2),
            "win": Discrete(2),
        }
        return action_spaces[agent]

    def render(self):
        if self.render_mode is None:
            logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return
        print(self.state)

    def close(self):
        pass

    def reset(self, seed=None, options=None):
        self.game = Game()
        self.game.init_game()
        next_step = self.game.next_step[0]
        agent = list(next_step.keys())[0]
        observations = self._get_observation(agent)
        infos = self._get_info(agent)
        self.agents = [agent]
        self.state = self.game.state
        if self.render_mode == "human":
            self.render()

        return observations, infos

    def step(self, actions):
        if not actions:
            return {}, {}, {}, {}, {}

        agent = list(actions.keys())[0]
        self.game.step(actions[agent])
        self.state = self.game.state
        if self.render_mode == "human":
            self.render()
        if self.game.next_step:
            next_step = self.game.next_step[0]
            agent = list(next_step.keys())[0]
            observations = self._get_observation(agent)
            rewards = self._get_reward(agent)
            terminations = self._get_termination(agent)
            infos = self._get_info(agent)
            if not terminations[agent]:
                self.agents = [agent]
                return (
                    observations,
                    rewards,
                    terminations,
                    {agent: False for agent in self.agents},
                    infos,
                )

        self.agents = []
        return {}, {}, {}, {}, {}

    def _get_observation(self, agent: str) -> dict[str, Any]:
        next_step = self.game.next_step[0]
        next_action = next_step[agent]
        action_type = next_action["type"]
        self_player = self.game.players[next_action["player"]]
        if agent == "discard":
            observation = self_player.hand.observation()
            for player in self.game.players:
                if player.turn == self_player.turn:
                    continue
                observation = np.concatenate((observation, player.declaration.observation()))
            observation = np.concatenate((observation, self.game.board.river_observation()))
            observations = {agent: {"observation": observation,
                                    "action_mask": self_player.hand.mask() if action_type == Action.DISCARD else None}}
        elif agent == "win":
            observation = self_player.hand.observation()
            observations = {agent: {"observation": observation,
                                    "action_mask": [1, 1]}}
        else:
            observation = self_player.hand.observation()
            observation = np.concatenate((observation, self_player.hand.claim_observation(next_action["tile"])))
            observations = {agent: {"observation": observation,
                                    "action_mask": [1, 1]}}
        return observations

    def _get_reward(self, agent: str) -> Dict[str, Any]:
        next_step = self.game.next_step[0]
        next_action = next_step[agent]
        self_player = self.game.players[next_action["player"]]
        rewards = {agent: self_player.hand.listen_count}
        return rewards

    def _get_info(self, agent: str) -> Dict[str, Any]:
        next_step = self.game.next_step[0]
        next_action = next_step[agent]
        self_player = self.game.players[next_action["player"]]
        if agent == "discard":
            dark_tiles = copy.deepcopy(self.game.board.wall)
            for player in self.game.players:
                if player.turn == self_player.turn:
                    continue
                dark_tiles.extend(copy.deepcopy(player.hand.tiles))
            return {agent: {
                "hand": sorted(copy.deepcopy(self_player.hand.tiles)),
                "dark": dark_tiles,
            }}
        elif agent == "win":
            return {agent: {}}
        else:
            claimed_hand = copy.deepcopy(self_player.hand.tiles)
            for tile in next_action["tile"]:
                if tile in claimed_hand:
                    claimed_hand.remove(tile)
            return {agent: {
                "hand": sorted(copy.deepcopy(self_player.hand.tiles)),
                "claimed_hand": sorted(claimed_hand)
            }}

    def _get_termination(self, agent: str) -> Dict[str, Any]:
        return {agent: self.game.over}
