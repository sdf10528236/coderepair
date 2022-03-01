import numpy as np
import pandas as pd
import string
import tensorflow as tf
from tensorflow import keras
import os

INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!"

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!"


max_input_length = 52
max_output_length = 50


def create_model():

    encoder_embedding_size = 32
    decoder_embedding_size = 32
    lstm_units = 128

    np.random.seed(42)
    tf.random.set_seed(42)

    encoder_input = keras.layers.Input(shape=[None], dtype=tf.int32)
    encoder_embedding = keras.layers.Embedding(
        input_dim=len(INPUT_CHARS) + 1,
        output_dim=encoder_embedding_size)(encoder_input)
    _, encoder_state_h, encoder_state_c = keras.layers.LSTM(
        lstm_units, return_state=True)(encoder_embedding)
    encoder_state = [encoder_state_h, encoder_state_c]

    decoder_input = keras.layers.Input(shape=[None], dtype=tf.int32)
    decoder_embedding = keras.layers.Embedding(
        input_dim=len(OUTPUT_CHARS) + 2,
        output_dim=decoder_embedding_size)(decoder_input)
    decoder_lstm_output = keras.layers.LSTM(lstm_units, return_sequences=True)(
        decoder_embedding, initial_state=encoder_state)
    decoder_output = keras.layers.Dense(len(OUTPUT_CHARS) + 1,
                                        activation="softmax")(decoder_lstm_output)
    model = keras.models.Model(inputs=[encoder_input, decoder_input],
                               outputs=[decoder_output])

    optimizer = keras.optimizers.Nadam()
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                  metrics=["accuracy"])

    return model


def data_str_to_ids(date_str, chars):

    return[chars.index(c) for c in date_str]


def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    X = tf.ragged.constant(X_ids, ragged_rank=1)
    return (X + 1).to_tensor()  # using 0 as the padding token ID


def create_dataset(x, y):

    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)


def ids_to_date_strs(ids, chars=OUTPUT_CHARS):
    return ["".join([(" " + chars)[index] for index in sequence])
            for sequence in ids]


def prepare_date_strs_padded(date_strs):
    X = prepare_date_strs(date_strs)
    if X.shape[1] < max_input_length:
        X = tf.pad(X, [[0, 0], [0, max_input_length - X.shape[1]]])
    return X


def convert_date_strs(date_strs):
    X = prepare_date_strs_padded(date_strs)
    pids = model.predict(X)
    ids = np.argmax(pids, axis=2)
    return ids_to_date_strs(ids)


sos_id = len(OUTPUT_CHARS) + 1


def predict_date_strs(date_strs, model):
    X = prepare_date_strs_padded(date_strs)
    Y_pred = tf.fill(dims=(len(X), 1), value=sos_id)
    for index in range(max_output_length):
        pad_size = max_output_length - Y_pred.shape[1]
        X_decoder = tf.pad(Y_pred, [[0, 0], [0, pad_size]])
        Y_probas_next = model.predict([X, X_decoder])[:, index:index+1]
        Y_pred_next = tf.argmax(Y_probas_next, axis=-1, output_type=tf.int32)
        Y_pred = tf.concat([Y_pred, Y_pred_next], axis=1)
    return ids_to_date_strs(Y_pred[:, 1:])


if __name__ == '__main__':
    latest = 'cp.ckpt'
    model = create_model()
    problem = 'printf(%d", score[j]);'
    model.load_weights(latest)
    ans = predict_date_strs([problem], model)[0]
    print(problem)
    print(ans)
