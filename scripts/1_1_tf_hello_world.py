import tensorflow as tf
import numpy as np


def house_model():
    xs = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype="float")
    ys = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5], dtype="float")

    # simplistic model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[1])
    ])

    # compiling...
    model.compile(optimizer="adam", loss="mse")

    # Training with 1000 epochs
    model.fit(xs, ys, epochs=1000)

    return model


if __name__ == "__main__":
    house_model()