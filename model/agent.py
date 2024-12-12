import keras
from keras import layers, Sequential

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
    model = Sequential()
    model.add(layers.InputLayer(input_shape=(12, 34, 1)))
    model.add(layers.Conv2D(256, (4, 1)))
    for _ in range(2):
        model.add(layers.Conv2D(256, (3, 1)))
        model.add(layers.Conv2D(256, (3, 1)))
    model.add(layers.Conv2D(1, (1, 1)))
    model.add(layers.Flatten())
    return model


def create_other_model():
    model = Sequential()
    model.add(layers.InputLayer(input_shape=(12, 34, 1)))
    model.add(layers.Conv2D(256, (3, 1)))
    for _ in range(2):
        model.add(layers.Conv2D(256, (3, 1)))
        model.add(layers.Conv2D(256, (3, 1)))
    model.add(layers.Conv2D(32, (1, 1)))
    model.add(layers.Flatten())
    model.add(layers.Dense(1024))
    model.add(layers.Dense(256))
    model.add(layers.Dense(2))
    return model


discard_model = create_discard_model()
chow_model = create_other_model()
pong_model = create_other_model()
kong_model = create_other_model()

target_discard_model = create_discard_model()
target_chow_model = create_other_model()
target_pong_model = create_other_model()
target_kong_model = create_other_model()

optimizer = keras.optimizers.Adam(lr=0.00025, clipnorm=1.0)

