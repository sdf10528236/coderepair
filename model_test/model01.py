import numpy as np
import pandas as pd
import string

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import os

gpus = tf.config.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.set_visible_devices(gpus[0], 'GPU')
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
  except RuntimeError as e:
    # Visible devices must be set before GPUs have been initialized
    print(e)

INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"
    
sos_id = len(OUTPUT_CHARS) + 1

def data_str_to_ids(date_str, chars):

    return [1+chars.index(c) for c in date_str]


def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    xlen = max(len(x) for x in X_ids)
    y = []
    for i in range(len(X_ids)):
        y.append(X_ids[i] + [0]*(xlen-len(X_ids[i])))

    return np.array(y)


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

def shifted_output_sequences(Y):
    Yshift = np.ones(Y.shape) * sos_id
    Yshift[:,1:] = Y[:,:-1]
    return Yshift
    # sos_tokens = tf.fill(dims=(len(Y), 1), value=sos_id)
    #print(Y)
    #print("sos=",sos_tokens)
    #print(tf.concat([sos_tokens, Y[:, :-1]], axis=1))
    # return tf.concat([sos_tokens, Y[:, :-1]], axis=1)



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
    df = pd.read_csv('../data/printf.csv')
    



    X_train, Y_train = create_dataset(df['wrong'][0:120000], df['correct'][0:120000])
    X_valid, Y_valid = create_dataset(df['wrong'][120000:135000], df['correct'][120000:135000])
    X_test, Y_test = create_dataset(df['wrong'][135000:150000], df['correct'][135000:150000])

    max_input_length = X_train.shape[1]
    

    X_train_decoder = shifted_output_sequences(Y_train)
    X_valid_decoder = shifted_output_sequences(Y_valid)
    x_test_decoder = shifted_output_sequences(Y_test)



    
    max_output_length = Y_train.shape[1]

    ################################################

    checkpoint_path = "training_2/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)



    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path, 
        verbose=1, 
        save_weights_only=True,
        save_freq = 'epoch' )

    ################################################
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
    #################################################
    model.save_weights(checkpoint_path.format(epoch=0))
    #################################################

    history = model.fit([X_train, X_train_decoder], Y_train, epochs=10,  callbacks=[cp_callback], 
                        validation_data=([X_valid, X_valid_decoder], Y_valid))