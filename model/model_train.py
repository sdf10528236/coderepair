import numpy as np
import pandas as pd
import string
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import tensorflow_addons as tfa
import os
from util.c_tokenizer import C_Tokenizer
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

tokenize = C_Tokenizer().tokenize

now_path = os.path.dirname(os.path.abspath(__file__))
INPUT_CHARS = np.load(now_path+'/all_dicts.npy',allow_pickle=True).item()
OUTPUT_CHARS = np.load(now_path+'/all_dicts.npy',allow_pickle=True).item()

sos_id = len(OUTPUT_CHARS) + 1


def data_str_to_token(data_str):
    #print(data_str)
    tokenized_code, name_dict, name_seq = tokenize(data_str)
    #print(tokenized_code, name_dict, name_seq)
    tokenized_code_list = tokenized_code.split()
    
        
    tokenized_code_list=[]
    #print(tokenized_code.split())
    for token in tokenized_code.split():
        
        if '_<id>_' in token:
            
            token = '_<id>_@'
            
        tokenized_code_list.append(token)
    return tokenized_code_list 
   
def data_str_to_ids(date_str, chars):
    tokenized_code_list = data_str_to_token(date_str)
    #print(tokenized_code_list)
    return [chars[f'{token}'] for token in tokenized_code_list]

def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    #print( X_ids)
    xlen = max(len(x) for x in X_ids)
    y = []
    for i in range(len(X_ids)):
        y.append(X_ids[i] + [0]*(xlen-len(X_ids[i])))
    #print(np.array(y))
    return np.array(y)
def create_dataset(x, y):
    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)


def shifted_output_sequences(Y):
    Yshift = np.ones(Y.shape) * sos_id
    Yshift[:,1:] = Y[:,:-1]
    return Yshift



def create_model():
    np.random.seed(42)
    tf.random.set_seed(42)

    encoder_embedding_size = 32
    decoder_embedding_size = 32
    units = 128

    encoder_inputs = keras.layers.Input(shape=[None], dtype=np.int32)
    decoder_inputs = keras.layers.Input(shape=[None], dtype=np.int32)
    sequence_lengths = keras.layers.Input(shape=[], dtype=np.int32)

    encoder_embeddings = keras.layers.Embedding(
        len(INPUT_CHARS) + 1, encoder_embedding_size)(encoder_inputs)

    decoder_embedding_layer = keras.layers.Embedding(
        len(INPUT_CHARS) + 2, decoder_embedding_size)
    decoder_embeddings = decoder_embedding_layer(decoder_inputs)

    encoder = keras.layers.LSTM(units, return_state=True)
    encoder_outputs, state_h, state_c = encoder(encoder_embeddings)
    encoder_state = [state_h, state_c]

    sampler = tfa.seq2seq.sampler.TrainingSampler()

    decoder_cell = keras.layers.LSTMCell(units)
    output_layer = keras.layers.Dense(len(OUTPUT_CHARS) + 1)

    decoder = tfa.seq2seq.basic_decoder.BasicDecoder(decoder_cell,
                                                    sampler,
                                                    output_layer=output_layer)
    final_outputs, final_state, final_sequence_lengths = decoder(
        decoder_embeddings,
        initial_state=encoder_state)
    Y_proba = keras.layers.Activation("softmax")(final_outputs.rnn_output)

    model = keras.models.Model(inputs=[encoder_inputs, decoder_inputs],
                            outputs=[Y_proba])
    optimizer = keras.optimizers.Nadam()
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                metrics=["accuracy"])
    return model


if __name__ == '__main__':
    df = pd.read_csv('../data/printf_autocreate.csv')
    X_train, Y_train = create_dataset(df['wrong'][0:70000], df['correct'][0:70000])
    X_valid, Y_valid = create_dataset(df['wrong'][70000:100000], df['correct'][70000:100000])
    

    max_input_length = X_train.shape[1]
    max_output_length = Y_train.shape[1]

    X_train_decoder = shifted_output_sequences(Y_train)
    X_valid_decoder = shifted_output_sequences(Y_valid)

    ################################################

    checkpoint_path = "training_token/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path, 
        verbose=1, 
        save_weights_only=True,
        save_freq = 'epoch' )

    ################################################
    model = create_model()
    #################################################
    model.save_weights(checkpoint_path.format(epoch=0))
    #################################################


    history = model.fit([X_train, X_train_decoder], Y_train, epochs=10, batch_size=256, callbacks=[cp_callback], 
                        validation_data=([X_valid, X_valid_decoder], Y_valid))