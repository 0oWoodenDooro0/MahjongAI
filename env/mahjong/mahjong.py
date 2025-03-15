import functools
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
        self.possible_agents = ["discard", "chow", "pong", "kong", "win"]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )
        self.render_mode = render_mode
        self.game = Game()

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        observation_spaces = {
            "discard": MultiDiscrete([20, 34]),
            "chow": MultiDiscrete([20, 34]),
            "pong": MultiDiscrete([20, 34]),
            "kong": MultiDiscrete([20, 34]),
            "win": MultiDiscrete([20, 34]),
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

    def close(self):
        pass

    def reset(self, seed=None, options=None):
        self.agents = ["discard"]
        self.game = Game()
        self.game.init_game()
        observations = self._get_observation("discard")
        infos = self._get_info("discard")
        if self.render_mode == "human":
            self.render()

        return observations, infos

    def step(self, actions):
        if not actions:
            return {}, {}, {}, {}, {}

        agent = list(actions.keys())[0]
        self.game.step(actions[agent])
        observations = self._get_observation(agent)
        rewards = self._get_reward(agent)
        terminations = self._get_termination(agent)
        infos = self._get_info(agent)
        if len(list(observations.keys())) == 0:
            self.agents = []
        else:
            self.agents = [list(observations.keys())[0]]

        if self.render_mode == "human":
            self.render()
        return (
            observations,
            rewards,
            terminations,
            {agent: False for agent in self.agents},
            infos,
        )

    def _get_observation(self, agent: str) -> dict[str, dict[str, ndarray[Any, dtype[Any]] | None]]:
        if not self.game.next_step:
            return {}
        next_step = self.game.next_step[0]
        agent = list(next_step.keys())[0]
        next_action = next_step[agent]
        action_type = next_action["type"]
        self_player = self.game.players[next_action["player"]]
        observation = self_player.hand.observation()
        for player in self.game.players:
            if player.turn == self_player.turn:
                continue
            observation = np.concatenate((observation, player.declaration.observation()))
        observation = np.concatenate((observation, self.game.board.river_observation()))
        observations = {agent: {"observation": observation,
                                "action_mask": self_player.hand.mask() if action_type == Action.DISCARD else None}}
        return observations

    def _get_reward(self, agent) -> Dict[Any, Any]:
        if len(self.game.next_step) == 0:
            return {}
        next_step = self.game.next_step[0]
        agent = list(next_step.keys())[0]
        next_action = next_step[agent]
        self_player = self.game.players[next_action["player"]]
        rewards = {agent: self_player.hand.listen_count}
        return rewards

    def _get_info(self, agent) -> Dict[Any, Any]:
        if len(self.game.next_step) == 0:
            return {}
        next_step = self.game.next_step[0]
        agent = list(next_step.keys())[0]
        next_action = next_step[agent]
        self_player = self.game.players[next_action["player"]]
        return {agent: {
            "hand": copy.deepcopy(self_player.hand)
        }}

    def _get_termination(self, agent) -> Dict[Any, Any]:
        return {agent: self.game.over}
