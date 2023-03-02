import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# callback
class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('accuracy') is not None and logs.get('accuracy') > 0.999:
            print("\nReached 99.9% accuracy so cancelling training!")
            self.model.stop_training = True


def image_generator():
    train_datagen = ImageDataGenerator(rescale=1 / 255)
    train_generator = train_datagen.flow_from_directory(
        directory="../data/hs/",
        target_size=(150, 150),
        batch_size=10,
        class_mode="binary"
    )

    return train_generator


def train_happy_sad_model(train_generator):

    # initialize callback
    callbacks = myCallback()

    # model architecture
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(150,150,3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    # compile model
    model.compile(loss="binary_crossentropy",
                  optimizer="adam",
                  metrics=['accuracy'])

    # training model
    history = model.fit(x=train_generator,
                        epochs=20,
                        callbacks=[callbacks]
                       )

    return history


if __name__ == "__main__":
    gen = image_generator()
    hist = train_happy_sad_model(gen)




