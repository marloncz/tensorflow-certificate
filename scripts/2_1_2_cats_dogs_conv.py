import os
import random
from shutil import copyfile

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def create_train_val_dirs(root_path):
    sub_folders = [
        "training/cats",
        "validation/cats",
        "training/dogs",
        "validation/dogs",
    ]

    for folder in sub_folders:
        os.makedirs(os.path.join(root_path, "cats-v-dogs", folder))


def split_data(source_dir, train_dir, val_dir, split_size):
    files = []

    for file_name in os.listdir(source_dir):
        path = source_dir + file_name

        if os.path.getsize(path):
            files.append(file_name)
        else:
            print(f"Size is 0 for {file_name}, ignoring file")

    n_files = len(files)
    split_index = int(n_files * split_size)
    files = random.sample(files, n_files)

    files_train = files[:split_index]
    files_test = files[split_index:]

    for file_name in files_train:
        copyfile(source_dir + file_name, train_dir + file_name)

    for file_name in files_test:
        copyfile(source_dir + file_name, val_dir + file_name)


def train_val_generators(train_dir, val_dir):
    # initialize ImageDataGenerator
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
    )

    # train_generator
    train_generator = train_datagen.flow_from_directory(
        directory=train_dir, batch_size=32, class_mode="binary", target_size=(150, 150)
    )

    # initialize ImageDataGenerator
    validation_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    # val_generator
    val_generator = validation_datagen.flow_from_directory(
        directory=val_dir, batch_size=32, class_mode="binary", target_size=(150, 150)
    )

    return train_generator, val_generator


def create_model():
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Conv2D(
                16, (3, 3), activation="relu", input_shape=(150, 150, 3)
            ),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    return model


if __name__ == "__main__":
    # downloaded images from https://www.microsoft.com/en-us/download/confirmation.aspx?id=54765
    source_path = "../data/PetImages"
    source_path_dogs = os.path.join(source_path, "Dog")
    source_path_cats = os.path.join(source_path, "Cat")

    # os.listdir returns a list containing all files under the given path
    print(f"There are {len(os.listdir(source_path_dogs))} images of dogs.")
    print(f"There are {len(os.listdir(source_path_cats))} images of cats.")

    # defining root dir
    root_dir = "../data"

    try:
        create_train_val_dirs(root_path=root_dir)
    except FileExistsError:
        print("File(s) already exists")

    # define paths
    cat_source_dir = "../data/PetImages/Cat/"
    dog_source_dir = "../data/PetImages/Dog/"

    train_dir = "../data/cats-v-dogs/training/"
    val_dir = "../data/cats-v-dogs/validation/"

    train_cats_dir = os.path.join(train_dir, "cats/")
    val_cats_dir = os.path.join(val_dir, "cats/")

    train_dogs_dir = os.path.join(train_dir, "dogs/")
    val_dogs_dir = os.path.join(val_dir, "dogs/")

    # Empty directories in case you run this cell multiple times
    if len(os.listdir(train_cats_dir)) > 0:
        for file in os.scandir(train_cats_dir):
            os.remove(file.path)
    if len(os.listdir(train_dogs_dir)) > 0:
        for file in os.scandir(train_dogs_dir):
            os.remove(file.path)
    if len(os.listdir(val_cats_dir)) > 0:
        for file in os.scandir(val_cats_dir):
            os.remove(file.path)
    if len(os.listdir(val_dogs_dir)) > 0:
        for file in os.scandir(val_dogs_dir):
            os.remove(file.path)

    # Define proportion of images used for training
    split_size = 0.9

    # splitting data
    split_data(cat_source_dir, train_cats_dir, val_cats_dir, split_size)
    split_data(dog_source_dir, train_dogs_dir, val_dogs_dir, split_size)

    print(f"Original cat's directory has {len(os.listdir(cat_source_dir))} images")
    print(f"Original dog's directory has {len(os.listdir(dog_source_dir))} images\n")

    # training and validation splits
    print(f"There are {len(os.listdir(train_cats_dir))} images of cats for training")
    print(f"There are {len(os.listdir(train_dogs_dir))} images of dogs for training")
    print(f"There are {len(os.listdir(val_cats_dir))} images of cats for validation")
    print(f"There are {len(os.listdir(val_dogs_dir))} images of dogs for validation")

    # creating train and val generator
    train_generator, val_generator = train_val_generators(train_dir, val_dir)

    # defining model
    model = create_model()

    # training model
    history = model.fit(train_generator, epochs=15, validation_data=val_generator)
