from abc import ABC
from typing import Dict, Any, List, Sequence

import numpy as np
from gymnasium.spaces import Discrete
from keras import saving

from mahjong import Hand, Tile


class Agent(ABC):
    def action(self, agent: str, action_space: Discrete, observation_space: Dict[str, Any],
               info: Dict[str, Hand | Any]) -> Sequence:
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
        return np.array([0, 1], dtype=np.int8)

    def tile_score(self, tiles: List[Tile], dark: List[Tile]) -> Sequence[int]:
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
        result = np.zeros(34)
        result[tiles[min_index]] = 1
        return result.astype(np.int8)


class RandomAgent(Agent):
    def action(self, observation_space: Dict[str, Any], action_space: Discrete, **kwargs):
        return observation_space['action_mask']


class ModelAgent(Agent):
    def __init__(self, discard_path: str):
        self.discard_model = saving.load_model(discard_path)

    def action(self, agent: str, observation_space: Dict[str, Any], **kwargs):
        if agent == "discard":
            predict = self.discard_model.predict(observation_space["observation"].reshape((1, 20, 34)),
                                                 verbose=0).reshape(34)
            predict = np.multiply(predict, observation_space["observation"][:][0][:])
            max_index = np.argmax(predict, axis=-1)
            predict = np.eye(predict.shape[-1], dtype=np.int8)[max_index]
            if not np.any(predict):
                print("random step")
                return observation_space['action_mask']
            return predict
        return np.array([0, 1], dtype=np.int8)
