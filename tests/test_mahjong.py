from unittest import TestCase

from pettingzoo.test import parallel_api_test

from env import mahjong_v0


class Test(TestCase):
    def test_parallel_env(self):
        env = mahjong_v0.parallel_env(render_mode="human")
        parallel_api_test(env, num_cycles=100)
