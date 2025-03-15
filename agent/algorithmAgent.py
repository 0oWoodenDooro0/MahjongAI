import copy
from typing import Dict, Any

from gymnasium.spaces import Discrete
from numpy import ndarray, dtype

from mahjong import Hand, Tile


class AlgorithmAgent(object):
    def action(self, agent: str, action_space: Discrete,
               observation_space: Dict[str, ndarray[Any, dtype[Any]] | None], info: Dict[str, Hand | Any]):
        if agent == "discard":
            action_mask = observation_space["action_mask"]
            hand = copy.deepcopy(info["hand"])
            min_listen_count = 13
            min_action = -1
            for i in range(len(action_mask)):
                if action_mask[i] == 1:
                    tiles = copy.copy(info["hand"].tiles)
                    tiles.remove(Tile(i))
                    hand.tiles = tiles
                    listen_count = hand.check_listen_count()
                    if listen_count < min_listen_count:
                        min_listen_count = listen_count
                        min_action = i
            return min_action
        return action_space.sample(observation_space['action_mask'])
