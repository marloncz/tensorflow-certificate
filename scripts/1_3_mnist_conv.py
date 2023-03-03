import numpy as np
import tensorflow as tf


# function for reshaping
def reshape_and_normalize(images):
    # Reshape the images to add an extra dimension
    images = np.reshape(images, (len(images), 28, 28, 1))

    # Normalize the pixel values
    images = images / 255.0

    return images


# defining callback
class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get("accuracy") is not None and logs.get("accuracy") >= 0.995:
            print("\nReached 99% accuracy so cancelling training!")

            # stop training if accuracy is 99.5 or above
            self.model.stop_training = True


def convolutional_model():
    # model architecture
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Conv2D(
                32, (3, 3), activation="relu", input_shape=(28, 28, 1)
            ),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )

    # Compile the model
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    # get train data
    (training_images, training_labels), _ = tf.keras.datasets.mnist.load_data()

    # normalize images for training
    training_images = reshape_and_normalize(training_images)

    # initialize model
    model = convolutional_model()

    # initialize callback
    callbacks = MyCallback()

    # model training
    history = model.fit(
        training_images, training_labels, epochs=10, callbacks=[callbacks]
    )
