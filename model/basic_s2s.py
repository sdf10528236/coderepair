import numpy as np
import regex
import string
import random
import pandas as pd
import tensorflow as tf
from tensorflow import keras

INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " (),;.\""

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " (),;.\""


def data_str_to_ids(date_str, chars):

    return [chars.index(c) for c in date_str]


def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    X = tf.ragged.constant(X_ids, ragged_rank=1)
    return (X + 1).to_tensor()  # using 0 as the padding token ID


def create_dataset(x, y):

    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)


def ids_to_date_strs(ids, chars=OUTPUT_CHARS):

    return ["".join([("?" + chars)[index] for index in sequence])
            for sequence in ids]


def prepare_date_strs_padded(date_strs):
    X = prepare_date_strs(date_strs)
    print(X)
    if X.shape[1] < max_input_length:
        X = tf.pad(X, [[0, 0], [0, max_input_length - X.shape[1]]])
    return X


if __name__ == '__main__':

    df = pd.read_csv('../data/printf.csv')

    print(INPUT_CHARS)
    X_train, Y_train = create_dataset(df['wrong'][:100], df['correct'][100])
    # print(X_train)

    max_input_length = X_train.shape[1]

    print(prepare_date_strs_padded([df['wrong'][1000], df['wrong'][1001]]))
    # print(ids_to_date_strs(X_train))
