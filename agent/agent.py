from typing import Any, Dict

from keras import Model, layers

from algorithmAgent import AlgorithmAgent, Agent, RandomAgent
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
    while env.agents:
        actions = {
            agent: _agent.action(agent=agent, action_space=env.action_space(agent),
                                 observation_space=observations[agent], info=infos[agent])
            for agent in env.agents
        }
        observations, rewards, terminations, truncations, infos = env.step(actions)
    state = env.state
    env.close()
    return state


def average(l):
    return sum(l) / len(l)


if __name__ == "__main__":
    times = 1000
    win_times = 0
    win_steps = []
    none_win_steps = []
    for i in range(times):
        state = run_in_agent(AlgorithmAgent())
        if state["win"]:
            win_times += 1
            win_steps.append(state["move_count"])
        else:
            none_win_steps.append(state["move_count"])

    print(f"{win_times=}")
    print(f"{average(win_steps)=}")
    print(f"{average(none_win_steps)=}")
