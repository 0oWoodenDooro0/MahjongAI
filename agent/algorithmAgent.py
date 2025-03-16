import copy
from abc import ABC
from typing import Dict, Any, List

from gymnasium.spaces import Discrete

from mahjong import Hand, Tile


class Agent(ABC):
    def action(self, agent: str, action_space: Discrete, observation_space: Dict[str, Any],
               info: Dict[str, Hand | Any]):
        raise NotImplementedError()


class AlgorithmAgent(Agent):
    def __init__(self):
        self.transfer_score = {
            0: 11,
            1: 12,
            2: 13,
            3: 14,
            4: 15,
            5: 16,
            6: 17,
            7: 18,
            8: 19,
            9: 31,
            10: 32,
            11: 33,
            12: 34,
            13: 35,
            14: 36,
            15: 37,
            16: 38,
            17: 39,
            18: 51,
            19: 52,
            20: 53,
            21: 54,
            22: 55,
            23: 56,
            24: 57,
            25: 58,
            26: 59,
            27: 71,
            28: 81,
            29: 91,
            30: 101,
            31: 111,
            32: 121,
            33: 131,
        }

    def action(self, agent: str, observation_space: Dict[str, Any], info: Dict[str, Hand | Any], **kwargs):
        if agent == "discard":
            return self.tile_score(info["hand"], info["dark"])
        return 1

    def tile_score(self, tiles: List[Tile], dark: List[Tile]) -> int:
        parameter = [10, 5, 1]
        scale = 50
        scores = []
        for tile in tiles:
            score = 0
            for tile2 in tiles:
                gap = abs(self.transfer_score[tile2] - self.transfer_score[tile])
                if gap < 3:
                    score += parameter[gap] * scale

            for tile2 in dark:
                gap = abs(self.transfer_score[tile2] - self.transfer_score[tile])
                if gap < 3:
                    score += parameter[gap]

            scores.append(score)

        min_index = scores.index(min(scores))
        return tiles[min_index]


class RandomAgent(Agent):
    def action(self, observation_space: Dict[str, Any], action_space: Discrete, **kwargs):
        return action_space.sample(observation_space['action_mask'])
