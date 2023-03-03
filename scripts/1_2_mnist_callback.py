import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten


class MyCallback(tf.keras.callbacks.Callback):
    # Define the correct function signature for on_epoch_end
    def on_epoch_end(self, epoch, logs={}):
        if logs.get("accuracy") is not None and logs.get("accuracy") > 0.99:
            print("\nReached 99% accuracy so cancelling training!")

            # Stop training once the above condition is met
            self.model.stop_training = True


def train_mnist(x_train, y_train):

    # Instantiate the callback class
    callbacks = MyCallback()

    # Model
    model = tf.keras.models.Sequential(
        [
            Flatten(input_shape=(28, 28)),
            Dense(512, activation="relu"),
            Dense(256, activation="relu"),
            Dense(10, activation="softmax"),
        ]
    )

    # print summary
    model.summary()

    # Compile the model
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Fit the model for 10 epochs adding the callbacks
    # and save the training history
    history = model.fit(x_train, y_train, epochs=10, callbacks=[callbacks])

    return history


if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # normalize data
    x_train, x_test = x_train / 255.0, x_test / 255.0

    data_shape = x_train.shape
    print(
        f"There are {data_shape[0]} examples with shape"
        + f"({data_shape[1]}, {data_shape[2]})"
    )

    hist = train_mnist(x_train, y_train)
