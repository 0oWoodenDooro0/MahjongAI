import os
from typing import Any, Dict, SupportsIndex, Sequence

import numpy as np
from keras import Model, layers, optimizers, saving, losses, callbacks, metrics
from tensorflow.data import Dataset

from algorithmAgent import Agent, AlgorithmAgent, ModelAgent
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
    dropout = layers.Dropout(0.2)(dense)
    outputs = layers.Softmax()(dropout)
    model = Model(inputs=inputs, outputs=outputs)
    return model


def load_model(path: str):
    if os.path.exists(path):
        model = saving.load_model(path)
        return model
    else:
        model = create_discard_model()
        return model


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


def load_np_data(path: str, shape: SupportsIndex | Sequence[SupportsIndex]):
    if os.path.exists(path=path):
        return np.load(file=path)
    else:
        return np.empty(shape=shape)


def make_train_data(agent: Agent, data_path: str, labels_path: str, times=1):
    win_times = 0
    win_steps = []
    none_win_steps = []
    discard_data = np.empty((0, 20, 34))
    discard_labels = np.empty((0, 34))
    for i in range(times):
        state = run_in_agent(agent)
        discard_data = np.append(discard_data, state["discard_input"], axis=0)
        discard_labels = np.append(discard_labels, state["discard_output"], axis=0)
        if state["win"]:
            win_times += 1
            win_steps.append(state["move_count"])
        else:
            none_win_steps.append(state["move_count"])
    np.save(data_path, discard_data)
    np.save(labels_path, discard_labels)

    print(f"{win_times=}")
    print(f"{average(win_steps)=}")
    print(f"{average(none_win_steps)=}")
    print(f"{len(discard_data)=}")


def run_agent_in_times(agent: Agent, times=1000):
    win_times = 0
    win_steps = []
    none_win_steps = []
    for i in range(times):
        state = run_in_agent(agent)
        if state["win"]:
            win_times += 1
            win_steps.append(state["move_count"])
        else:
            none_win_steps.append(state["move_count"])
    print(f"{win_times=}")
    print(f"{average(win_steps)=}")
    print(f"{average(none_win_steps)=}")


def train(data_path, labels_path, lr=0.001, epochs=1, batch_size=None):
    discard_input_data = load_np_data(data_path, (0, 20, 34))
    discard_output_data = load_np_data(labels_path, (0, 34))

    train_discard_dataset, validation_discard_dataset, test_discard_dataset = split_data(discard_input_data,
                                                                                         discard_output_data)

    train_discard_dataset = train_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)
    validation_discard_dataset = validation_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)
    test_discard_dataset = test_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)

    tensorboard_callback = callbacks.TensorBoard(log_dir="../data/logs")

    discard_model = load_model("../data/discard_model.keras")
    # learning_rate_schedule = optimizers.schedules.CosineDecay(initial_learning_rate=lr, decay_steps=1000,
    #                                                           warmup_steps=1000, warmup_target=lr)
    optimizer = optimizers.Adam(learning_rate=lr)
    discard_model.compile(optimizer=optimizer, loss=losses.CategoricalCrossentropy(),
                          metrics=[metrics.CategoricalAccuracy()])
    early_stopping = callbacks.EarlyStopping(monitor="val_categorical_accuracy", mode="max", patience=10, restore_best_weights=True)
    reduce_lr = callbacks.ReduceLROnPlateau(monitor="val_categorical_accuracy", mode="max", factor=0.1, patience=5, min_lr=1e-6)
    discard_model.fit(train_discard_dataset, epochs=epochs, validation_data=validation_discard_dataset,
                      callbacks=[tensorboard_callback, early_stopping, reduce_lr])
    discard_model.save("../data/discard_model.keras")
    loss, accuracy = discard_model.evaluate(test_discard_dataset)
    print(f"{loss=}")
    print(f"{accuracy=}")


def split_data(data: np.ndarray, labels: np.ndarray, test_rate=0.2, validation_rate=0.1):
    dataset_size = len(labels)
    dataset = Dataset.from_tensor_slices((data, labels))
    test_size = int(dataset_size * test_rate)
    validation_size = int(dataset_size * validation_rate)
    train_size = dataset_size - test_size - validation_size

    train_dataset = dataset.take(train_size)
    validation_dataset = dataset.skip(train_size).take(validation_size)
    test_dataset = dataset.skip(train_size + validation_size).take(test_size)

    return train_dataset, validation_dataset, test_dataset


def get_train_data_info(discard_output_data):
    ones_indices = np.argmax(discard_output_data, axis=1)
    unique_indices, counts = np.unique(ones_indices, return_counts=True)

    all_counts = np.zeros(34, dtype=int)
    all_counts[unique_indices] = counts
    print(all_counts)
    print(len(discard_output_data))


if __name__ == "__main__":
    # make_train_data(AlgorithmAgent(), data_path="../data/discard_data1.npy", labels_path="../data/discard_labels1.npy",
    #                 times=2000)
    # train(data_path="../data/discard_data1.npy", labels_path="../data/discard_labels1.npy", lr=0.01, epochs=64,
    #       batch_size=32)
    run_agent_in_times(ModelAgent(discard_path="../data/discard_model.keras"), times=100)
    # get_train_data_info(load_np_data("../data/discard_output.npy", (0, 34)))
