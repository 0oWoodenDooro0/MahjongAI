import functools

from gymnasium import logger
from gymnasium.spaces import Discrete, MultiDiscrete
from pettingzoo.utils.env import ParallelEnv

from mahjong import Game


def parallel_env(render_mode=None):
    return MahjongParallelEnv(render_mode=render_mode)


class MahjongParallelEnv(ParallelEnv):
    metadata = {"render_mode": ["human"], "name": "majhong_env_v0"}

    def __init__(self, render_mode=None):
        self.possible_agents = ["discard", "chow", "pong", "kong", "win"]
        self.agent_name_mapping = dict(zip(self.possible_agents, list(range(len(self.possible_agents)))))
        self.render_mode = render_mode
        self.game = Game()

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        observation_spaces = {
            "discard": MultiDiscrete([20, 34]),
            "chow": MultiDiscrete([20, 34]),
            "pong": MultiDiscrete([20, 34]),
            "kong": MultiDiscrete([20, 34]),
            "win": MultiDiscrete([20, 34])
        }
        return observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        action_spaces = {
            "discard": Discrete(34),
            "chow": Discrete(2),
            "pong": Discrete(2),
            "kong": Discrete(2),
            "win": Discrete(2)
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
        self.num_moves = 0
        observations, infos = self.game.init_game()
        self.state = observations

        return observations, infos

    def step(self, actions):
        if not actions:
            return {}, {}, {}, {}, {}

        agent = list(actions.keys())[0]
        observations, rewards, terminations, infos = self.game.step(actions[agent])
        if len(list(observations.keys())) == 0:
            self.agents = []
        else:
            self.agents = [list(observations.keys())[0]]

        if self.render_mode == "human":
            self.render()
        return observations, rewards, terminations, {agent: False for agent in self.agents}, infos
