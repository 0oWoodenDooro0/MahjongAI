import functools

from gymnasium import logger
from gymnasium.spaces import Discrete
from pettingzoo import ParallelEnv
from pettingzoo.utils import wrappers

from mahjong import Game, Action, Tile


def env(render_mode=None):
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = MahjongEnv(render_mode=internal_render_mode)
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class MahjongEnv(ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "majhong_env"}

    def __init__(self, render_mode=None):
        self.possible_agents = ["discard", "chow", "pong", "kong", "win"]
        self.agent_name_mapping = dict(zip(self.possible_agents, list(range(len(self.possible_agents)))))
        self.render_mode = render_mode
        self.game = Game()

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        observation_spaces = {
            "discard": Discrete(272),
            "chow": Discrete(272),
            "pong": Discrete(272),
            "kong": Discrete(272),
            "win": Discrete(272)
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

        for player in self.game.players:
            print(sorted(player.hand), len(player.hand))
        return

    def close(self):
        print("Game Over")
        return

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self.game = Game()
        observations, infos = self.game.init_game()
        self.state = observations
        return observations, infos

    def step(self, action):
        if not action:
            return None

        agent = list(action.keys())[0]
        if agent == "discard":
            observations, rewards, terminations, infos = self.game.step(Action.DISCARD, action[agent]["player"],
                                                                        (Tile(action[agent]["action"]),))
        elif action[agent]["action"] == 0:
            print("nothing")
            observations, rewards, terminations, infos = self.game.step(Action.NOTHING, action[agent]["player"], None)
        elif agent == "chow":
            observations, rewards, terminations, infos = self.game.step(Action.CHOW, action[agent]["player"],
                                                                        action[agent]["tile"])
        elif agent == "pong":
            observations, rewards, terminations, infos = self.game.step(Action.PONG, action[agent]["player"],
                                                                        action[agent]["tile"])
        elif agent == "kong":
            if action[agent]["type"] == "kong":
                observations, rewards, terminations, infos = self.game.step(Action.KONG, action[agent]["player"],
                                                                            action[agent]["tile"])
            elif action[agent]["type"] == "add_kong":
                observations, rewards, terminations, infos = self.game.step(Action.ADDKONG, action[agent]["player"],
                                                                            action[agent]["tile"])
            elif action[agent]["type"] == "closed_kong":
                observations, rewards, terminations, infos = self.game.step(Action.CLOSEDKONG, action[agent]["player"],
                                                                            action[agent]["tile"])
        elif agent == "win":
            observations, rewards, terminations, infos = self.game.step(Action.WIN, action[agent]["player"],
                                                                        action[agent]["tile"])

        if self.render_mode == "human":
            self.render()
        return observations, rewards, terminations, False, infos
