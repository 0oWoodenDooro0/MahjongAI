import os
from typing import Any, Dict, Tuple, SupportsIndex, Sequence

import numpy as np
from keras import Model, layers

from algorithmAgent import AlgorithmAgent, Agent
from env import mahjong_v0

SEED = 42
GAMMA = 0.99
EPSILON = 1.0
EPSILON_MIN = 0.1
EPSILON_MAX = 1.0
EPSILONl_INTERVAL = EPSILON_MAX - EPSILON_MIN
BATCH_SIZE = 32
MAX_STEPS_PER_EPISODE = 1000
MAX_EPISODES = 1000


def create_discard_model():
    inputs = layers.Input(shape=(20, 34))
    reshape = layers.Reshape((20, 34, 1))(inputs)
    conv2d_1 = layers.Conv2D(256, (4, 1))(reshape)
    state = conv2d_1
    for _ in range(50):
        conv2d_2 = layers.Conv2D(256, (3, 1), strides=1, padding="same")(state)
        bactch_normalize_1 = layers.BatchNormalization()(conv2d_2)
        activation = layers.ReLU()(bactch_normalize_1)
        conv2d_3 = layers.Conv2D(256, (3, 1), padding="same")(activation)
        bactch_normalize_2 = layers.BatchNormalization()(conv2d_3)
        state = layers.add([state, bactch_normalize_2])
        state = layers.ReLU()(state)
    conv2d_4 = layers.Conv2D(1, (1, 1))(state)
    flatten = layers.Flatten()(conv2d_4)
    dense = layers.Dense(34)(flatten)
    masked_output = layers.Lambda(lambda x: x, mask=inputs[:, 0, :])(dense)
    outputs = layers.Softmax()(masked_output)
    model = Model(inputs=inputs, outputs=outputs)
    return model


# discard_model = create_discard_model()
# discard_model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
# discard_model.summary()

def run_in_agent(_agent: Agent, render_mode=None) -> Dict[str, Any]:
    env = mahjong_v0.parallel_env(render_mode)
    observations, infos = env.reset()
    discard_input = []
    discard_output = []
    while env.agents:
        action_predict = {
            agent: _agent.action(agent=agent, action_space=env.action_space(agent),
                                 observation_space=observations[agent], info=infos[agent])
            for agent in env.agents
        }
        actions = {
            agent: env.action_space(agent).sample(action_predict[agent])
            for agent in env.agents
        }
        for agent in env.agents:
            if agent == "discard":
                discard_input.append(observations[agent]["observation"])
                discard_output.append(action_predict[agent])
        observations, rewards, terminations, truncations, infos = env.step(actions)
    state = env.state
    state["discard_input"] = discard_input
    state["discard_output"] = discard_output
    env.close()
    return state


def average(l):
    if len(l) == 0:
        return 0
    return sum(l) / len(l)


def load_data(path: str, shape: SupportsIndex | Sequence[SupportsIndex]):
    if os.path.exists(path=path):
        return np.load(file=path)
    else:
        return np.empty(shape=shape)


if __name__ == "__main__":
    times = 1000
    win_times = 0
    win_steps = []
    none_win_steps = []
    discard_input = load_data("../data/discard_input.npy", (0, 20, 34))
    discard_output = load_data("../data/discard_output.npy", (0, 34))
    for i in range(times):
        state = run_in_agent(AlgorithmAgent())
        discard_input = np.append(discard_input, state["discard_input"], axis=0)
        discard_output = np.append(discard_output, state["discard_output"], axis=0)
        if state["win"]:
            win_times += 1
            win_steps.append(state["move_count"])
        else:
            none_win_steps.append(state["move_count"])
    np.save("../data/discard_input.npy", discard_input)
    np.save("../data/discard_output.npy", discard_output)

    print(f"{win_times=}")
    print(f"{average(win_steps)=}")
    print(f"{average(none_win_steps)=}")
    print(discard_input.shape)
    print(discard_output.shape)
