import numpy as np
from keras import layers, Model

from env import MahjongEnv

SEED = 42
GAMMA = 0.99
EPSILON = 1.0
EPSILON_MIN = 0.1
EPSILON_MAX = 1.0
EPSILONl_INTERVAL = (EPSILON_MAX - EPSILON_MIN)
BATCH_SIZE = 32
MAX_STEPS_PER_EPISODE = 1000
MAX_EPISODES = 1000


def create_discard_model():
    inputs = layers.Input(shape=(20, 34))
    reshape = layers.Reshape((20, 34, 1))(inputs)
    conv2d_1 = layers.Conv2D(256, (4, 1))(reshape)
    state = conv2d_1
    for _ in range(50):
        conv2d_2 = layers.Conv2D(256, (3, 1), strides=1, padding='same')(state)
        bactch_normalize_1 = layers.BatchNormalization()(conv2d_2)
        activation = layers.ReLU()(bactch_normalize_1)
        conv2d_3 = layers.Conv2D(256, (3, 1), padding='same')(activation)
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


discard_model = create_discard_model()
discard_model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
discard_model.summary()

env = MahjongEnv(render_mode="human")
observations, infos = env.reset()
while True:
    agent = list(infos.keys())[0]
    predict = None
    if agent == "discard":
        predict = np.argmax(discard_model.predict(observations["observation"].reshape((1, 20, 34)))[0])
    else:
        predict = env.action_space(agent).sample(None)
    action = {agent: {"action": predict, "player": infos[agent]["player"], "tile": infos[agent]["tile"],
                      "type": infos[agent].get("type", None)}}
    observations, rewards, terminations, trucations, infos = env.step(action)
    if terminations:
        break
env.close()
