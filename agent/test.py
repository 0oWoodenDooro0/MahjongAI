from env import MahjongEnv
from pettingzoo.test import parallel_api_test

env = MahjongEnv()
parallel_api_test(env, num_cycles=10)
