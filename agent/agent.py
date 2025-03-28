import os
from typing import Any, Dict, SupportsIndex, Sequence

import numpy as np
from keras import Model, layers, optimizers, saving, losses, callbacks, metrics
from tensorflow.data import Dataset

from algorithmAgent import Agent, ModelAgent, RandomAgent
from algorithmAgent import AlgorithmAgent
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
    data = {}
    labels = {}
    data["discard"] = np.empty((0, 20, 34))
    labels["discard"] = np.empty((0, 34))
    data["chow"] = np.empty((0, 8, 34))
    labels["chow"] = np.empty((0, 2))
    data["pong"] = np.empty((0, 8, 34))
    labels["pong"] = np.empty((0, 2))
    data["kong"] = np.empty((0, 8, 34))
    labels["kong"] = np.empty((0, 2))
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
            if agent != "win":
                shape = observations[agent]["observation"].shape
                data[agent] = np.append(data[agent], observations[agent]["observation"].reshape((1, shape[0], shape[1])), axis=0)
                shape = action_predict[agent].shape
                labels[agent] = np.append(labels[agent], action_predict[agent].reshape((1, shape[0])), axis=0)
        observations, rewards, terminations, truncations, infos = env.step(actions)
    state = env.state
    state["data"] = data
    state["labels"] = labels
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
    chow_data = np.empty((0, 8, 34))
    chow_labels = np.empty((0, 2))
    pong_data = np.empty((0, 8, 34))
    pong_labels = np.empty((0, 2))
    kong_data = np.empty((0, 8, 34))
    kong_labels = np.empty((0, 2))
    for i in range(times):
        state = run_in_agent(agent)
        data = state["data"]
        labels = state["labels"]
        discard_data = np.append(discard_data, data["discard"], axis=0)
        discard_labels = np.append(discard_labels, labels["discard"], axis=0)
        chow_data = np.append(chow_data, data["chow"], axis=0)
        chow_labels = np.append(chow_labels, labels["chow"], axis=0)
        pong_data = np.append(pong_data, data["pong"], axis=0)
        pong_labels = np.append(pong_labels, labels["pong"], axis=0)
        kong_data = np.append(kong_data, data["kong"], axis=0)
        kong_labels = np.append(kong_labels, labels["kong"], axis=0)
        if state["win"]:
            win_times += 1
            win_steps.append(state["move_count"])
        else:
            none_win_steps.append(state["move_count"])
    np.save(data_path + "discard_data.npy", discard_data)
    np.save(labels_path + "discard_labels.npy", discard_labels)
    np.save(data_path + "chow_data.npy", chow_data)
    np.save(labels_path + "chow_labels.npy", chow_labels)
    np.save(data_path + "pong_data.npy", pong_data)
    np.save(labels_path + "pong_labels.npy", pong_labels)
    np.save(data_path + "kong_data.npy", kong_data)
    np.save(labels_path + "kong_labels.npy", kong_labels)

    print(f"{win_times=}")
    print(f"{average(win_steps)=}")
    print(f"{average(none_win_steps)=}")
    print(f"{len(discard_data)=}")
    print(f"{len(chow_data)=}")
    print(f"{len(pong_data)=}")
    print(f"{len(kong_data)=}")


def run_agent_in_times(agent: Agent, times=1000, render_mode=None):
    win_times = 0
    win_steps = []
    none_win_steps = []
    for i in range(times):
        state = run_in_agent(agent, render_mode=render_mode)
        if state["win"]:
            win_times += 1
            win_steps.append(state["move_count"])
        else:
            none_win_steps.append(state["move_count"])
    print(f"{win_times=}")
    print(f"{average(win_steps)=}")
    print(f"{average(none_win_steps)=}")


def train(data_path, labels_path, model_path, lr=0.001, epochs=1, batch_size=None):
    discard_input_data = load_np_data(data_path, (0, 20, 34))
    discard_output_data = load_np_data(labels_path, (0, 34))

    train_discard_dataset, validation_discard_dataset, test_discard_dataset = split_data(discard_input_data,
                                                                                         discard_output_data)

    train_discard_dataset = train_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)
    validation_discard_dataset = validation_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)
    test_discard_dataset = test_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)

    tensorboard_callback = callbacks.TensorBoard(log_dir="../data/logs")

    discard_model = load_model(model_path)
    # learning_rate_schedule = optimizers.schedules.CosineDecay(initial_learning_rate=lr, decay_steps=1000,
    #                                                           warmup_steps=1000, warmup_target=lr)
    optimizer = optimizers.Adam(learning_rate=lr)
    discard_model.compile(optimizer=optimizer, loss=losses.CategoricalCrossentropy(),
                          metrics=[metrics.CategoricalAccuracy()])
    early_stopping = callbacks.EarlyStopping(monitor="val_categorical_accuracy", mode="max", patience=10,
                                             restore_best_weights=True)
    reduce_lr = callbacks.ReduceLROnPlateau(monitor="val_categorical_accuracy", mode="max", factor=0.1, patience=5,
                                            min_lr=1e-6)
    discard_model.fit(train_discard_dataset, epochs=epochs, validation_data=validation_discard_dataset,
                      callbacks=[tensorboard_callback, early_stopping, reduce_lr])
    discard_model.save(model_path)
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


def get_train_data_info(path):
    discard_data = load_np_data(path + "discard_labels.npy", (0, 34))
    chow_data = load_np_data(path + "chow_labels.npy", (0, 2))
    pong_data = load_np_data(path + "pong_labels.npy", (0, 2))
    kong_data = load_np_data(path + "kong_labels.npy", (0, 2))

    ones_indices = np.argmax(discard_data, axis=1)
    unique_indices, counts = np.unique(ones_indices, return_counts=True)

    all_counts = np.zeros(34, dtype=int)
    all_counts[unique_indices] = counts
    print(all_counts)
    print(f"{len(discard_data)=}")
    print(f"{len(chow_data)=}")
    print(f"{len(pong_data)=}")
    print(f"{len(kong_data)=}")


def test_data(data_path, labels_path, model_path, batch_size=32):
    discard_input_data = load_np_data(data_path, (0, 20, 34))
    discard_output_data = load_np_data(labels_path, (0, 34))
    train_discard_dataset, validation_discard_dataset, test_discard_dataset = split_data(discard_input_data,
                                                                                         discard_output_data)

    test_discard_dataset = test_discard_dataset.shuffle(buffer_size=1024).batch(batch_size)
    discard_model = load_model(model_path)
    loss, accuracy = discard_model.evaluate(test_discard_dataset)
    print(f"{loss=}")
    print(f"{accuracy=}")


if __name__ == "__main__":
    # run_in_agent(AlgorithmAgent(), "human")
    # make_train_data(AlgorithmAgent(), data_path="../data/data/", labels_path="../data/labels/", times=2000)
    # get_train_data_info("../data/labels/")
    # train(data_path="../data/discard_data1.npy", labels_path="../data/discard_labels1.npy",
    #       model_path="../data/discard_model.keras", lr=0.01, epochs=128, batch_size=32)
    # test_data(data_path="../data/discard_data1.npy", labels_path="../data/discard_labels1.npy",
    #           model_path="../data/discard_model.keras")
    # run_agent_in_times(ModelAgent(discard_path="../data/discard_model.keras"), times=1)
    pass
