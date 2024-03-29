import regex
from difflib import SequenceMatcher
import subprocess
import pandas as pd
import string
import numpy as np
import tensorflow as tf 
from tensorflow import keras
import os

INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"
sos_id = len(OUTPUT_CHARS) + 1

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

def run_compiler(filepath, compiler_path="gcc"):
    p = subprocess.run(
        [compiler_path, filepath], capture_output=True)

    warning_text = p.stderr.decode("utf-8").splitlines()
    return warning_text


def column_fix(old_file, new_file, column):
    line_column = 1
    file_data = ""
    checkpoint_path = "training_2/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    with open(old_file, "r") as f:

        for line in f:
            if str(line_column) == column:
                printf_positions = [m.span()
                                    for m in regex.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    
                    
                    model = create_model()
                    model.load_weights(latest)
                    
                    fix_line = predict_date_strs(
                        [line[printf_positions[0][0]:]], model)[0]

                    line = line[:printf_positions[0][0]] + \
                        fix_line + "\n"

            file_data += line

            line_column = line_column+1
        # print(file_data)
    with open(new_file, "w") as f:
        f.write(file_data)


def find_column(warning_text, filename):
    for text in warning_text:

        p = [m.span()for m in regex.finditer('error', text)]
        if(len(p) != 0):
            # print(text)
            colon_positions = [m.span()
                               for m in regex.finditer(":", text)]  # 冒號位置
            colume_start = [m.span()
                            for m in regex.finditer(f"{filename}:", text)]
            column_end = min((i[0] for i in colon_positions if i[0] >
                              colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))

            column = text[colume_start[0][1]:column_end]
            break

    return column


def auto_model_fix(folder_path, filename):
    warning_text = run_compiler(folder_path)

    column = find_column(warning_text, filename)
    column_fix(folder_path, folder_path, column)

def create_dataset(x, y):

    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)

def data_str_to_ids(date_str, chars):

    return [1+chars.index(c) for c in date_str]

def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    xlen = max(len(x) for x in X_ids)
    y = []
    for i in range(len(X_ids)):
        y.append(X_ids[i] + [0]*(xlen-len(X_ids[i])))

    return np.array(y)

def ids_to_date_strs(ids, chars=OUTPUT_CHARS):
    return ["".join([(" " + chars)[index] for index in sequence])
            for sequence in ids]

def prepare_date_strs_padded(date_strs):
    X = prepare_date_strs(date_strs)
    if X.shape[1] < max_input_length:
        X = tf.pad(X, [[0, 0], [0, max_input_length - X.shape[1]]])
    return X

def predict_date_strs(date_strs):
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
   

<<<<<<< HEAD
    checkpoint_path = "training_Shuffle/cp-{epoch:04d}.ckpt"
=======
    checkpoint_path = "training_noS_15000/cp-{epoch:04d}.ckpt"
>>>>>>> 1793f821fc39a9cb01ce84da9881aa6a751d224b
    checkpoint_dir = os.path.dirname(checkpoint_path)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    print(latest)


    model = create_model()
    model.load_weights(latest)
    df = pd.read_csv('../data/printf_codinghere_Shuffle.csv')
    
    X_train, Y_train = create_dataset(df['wrong'][0:10000], df['correct'][0:10000])
    X_valid, Y_valid = create_dataset(df['wrong'][10000:12500], df['correct'][10000:12500])
    X_test, Y_test = create_dataset(df['wrong'][12500:15000], df['correct'][12500:15000])

    max_input_length = X_train.shape[1]
    max_output_length = Y_train.shape[1]

    # print([df['wrong'][1410],df['wrong'][1611]])
    # print(predict_date_strs([df['wrong'][1410],df['wrong'][1611]])) 
    filename = "c1.c"
    folder_path = f'../data/correct_data/{filename}'
    

    warning_text = run_compiler(folder_path)

    column = find_column(warning_text, filename)
    file_data = ""
    line_column = 1
    with open(folder_path, "r") as f:

        for line in f:
            if str(line_column) == column:
                printf_positions = [m.span()
                                    for m in regex.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    
                    
                    model = create_model()
                    model.load_weights(latest)
                    print(line[printf_positions[0][0]:])
                    wrong_str = line[printf_positions[0][0]:]
                    fixed_str = predict_date_strs([wrong_str])[0]
                    print(fixed_str)
                    # fix_line = predict_date_strs(
                    #     [line[printf_positions[0][0]:]], model)[0]

                    # line = line[:printf_positions[0][0]] + \
                    #     fix_line + "\n"

            file_data += line

            line_column = line_column+1
        # print(file_data)