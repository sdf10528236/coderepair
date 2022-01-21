import numpy as np
import regex
import string
import random
import pandas as pd
import tensorflow as tf

INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " (),;.\""

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " (),;.\""


def data_str_to_ids(date_str, chars):

    return [chars.index(c) for c in date_str]


def prepare_date_strs(data_strs, chars):
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    X = tf.ragged.constant(X_ids, ragged_rank=1)
    return (X + 1).to_tensor()  # using 0 as the padding token ID


def create_dataset(x, y):

    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)


if __name__ == '__main__':

    df = pd.read_csv('../data/printf.csv')

    print(INPUT_CHARS)
    for cur_line_str in df['wrong'][:20]:
        print(create_dataset(cur_line_str, INPUT_CHARS))
    for cur_line_str in df['correct'][:20]:
        print(create_dataset(cur_line_str, OUTPUT_CHARS))
