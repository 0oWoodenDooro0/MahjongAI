import warnings
from unittest import TestCase

from pettingzoo import ParallelEnv
from pettingzoo.test.api_test import missing_attr_warning
from pettingzoo.test.parallel_test import sample_action
from pettingzoo.utils import BaseWrapper
from pettingzoo.utils.conversions import aec_to_parallel_wrapper, parallel_to_aec_wrapper, \
    turn_based_aec_to_parallel_wrapper

from env import mahjong_v0


class Test(TestCase):

    def parallel_api_test(self, par_env: ParallelEnv, num_cycles=1000):
        par_env.max_cycles = num_cycles

        if not hasattr(par_env, "possible_agents"):
            warnings.warn(missing_attr_warning.format(name="possible_agents"))

        assert not isinstance(par_env.unwrapped, aec_to_parallel_wrapper)
        assert not isinstance(par_env.unwrapped, parallel_to_aec_wrapper)
        assert not isinstance(par_env.unwrapped, turn_based_aec_to_parallel_wrapper)
        assert not isinstance(par_env.unwrapped, BaseWrapper)

        # checks that reset takes arguments seed and options
        par_env.reset(seed=0, options={"options": 1})

        MAX_RESETS = 2
        for _ in range(MAX_RESETS):
            obs, infos = par_env.reset()

            assert isinstance(obs, dict)
            assert isinstance(infos, dict)
            # Note: obs and info dicts must contain all AgentIDs, but can also have other additional keys (e.g., "common")
            assert set(par_env.agents).issubset(set(obs.keys()))
            assert set(par_env.agents).issubset(set(infos.keys()))
            terminated = {agent: False for agent in par_env.agents}
            truncated = {agent: False for agent in par_env.agents}
            for _ in range(num_cycles):
                actions = {
                    agent: sample_action(par_env, obs, agent)
                    for agent in par_env.agents
                    if (
                            (agent in terminated and not terminated[agent])
                            or (agent in truncated and not truncated[agent])
                    )
                }
                obs, rew, terminated, truncated, info = par_env.step(actions)

                assert isinstance(obs, dict)
                assert isinstance(rew, dict)
                assert isinstance(terminated, dict)
                assert isinstance(truncated, dict)
                assert isinstance(info, dict)

                if hasattr(par_env, "possible_agents"):
                    assert set(par_env.agents).issubset(
                        set(par_env.possible_agents)
                    ), "possible_agents defined but does not contain all agents"

                elif not par_env.agents:
                    warnings.warn("No agents present")

                for agent in par_env.agents:
                    assert par_env.observation_space(agent) is par_env.observation_space(
                        agent
                    ), "observation_space should return the exact same space object (not a copy) for an agent. Consider decorating your observation_space(self, agent) method with @functools.lru_cache(maxsize=None)"
                    assert par_env.action_space(agent) is par_env.action_space(
                        agent
                    ), "action_space should return the exact same space object (not a copy) for an agent (ensures that action space seeding works as expected). Consider decorating your action_space(self, agent) method with @functools.lru_cache(maxsize=None)"

        print("Passed Parallel API test")

    def test_parallel_env(self):
        env = mahjong_v0.parallel_env(render_mode="human")
        self.parallel_api_test(env)
