import regex
import subprocess
import pandas as pd
import string
import numpy as np
import tensorflow as tf 
import os
from model_train import create_model 
from util.c_tokenizer import C_Tokenizer
import difflib




tokenize = C_Tokenizer().tokenize
INPUT_CHARS = np.load('all_dicts.npy',allow_pickle=True).item()
OUTPUT_CHARS = np.load('all_dicts.npy',allow_pickle=True).item()
id_to_token_dict = {v:k for k,v in INPUT_CHARS.items()}
    
sos_id = len(OUTPUT_CHARS) + 1




def run_compiler(filepath, compiler_path="gcc"):
    p = subprocess.run(
        [compiler_path, filepath], capture_output=True)

    warning_text = p.stderr.decode("utf-8").splitlines()
    return warning_text




def find_column(warning_text, filename):
    column = []
    #print(warning_text)
    for text in warning_text:
       
       
        p = [m.span()for m in regex.finditer('error', text)]

        if(len(p) > 0):
            # print(text)
            colon_positions = [m.span()
                               for m in regex.finditer(":", text)]  # 冒號位置
            
            colume_start = [m.span()
                            for m in regex.finditer(f"{filename}:", text)]
            #print(colume_start)
            if (len(colume_start)>0) :
                column_end = min((i[0] for i in colon_positions if i[0] >
                              colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))
                n = text[colume_start[0][1]:column_end]
          
                if n not in column:
                    column.append(text[colume_start[0][1]:column_end]) 
            else: 
                continue
            
            
    #print(column)
    return column

def data_str_to_token(data_str):
    #print(data_str)
    tokenized_code, name_dict, name_seq = tokenize(data_str)
   
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

def prepare_data(data_strs, chars=INPUT_CHARS):
    
    X_ids = [data_str_to_ids(data_strs, chars)]
    
    xlen = max(len(x) for x in X_ids)
    y = []
    for i in range(len(X_ids)):
        y.append(X_ids[i] + [0]*(xlen-len(X_ids[i])))
    #print(np.array(y))
    return np.array(y)

def create_dataset(x, y):
    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)



def ids_to_token(ids, chars=id_to_token_dict):
    #print(ids)
       
    return [" ".join(chars[index] for index in sequence)for sequence in ids]



def tokens_to_source(tokens, name_dict, clang_format=False, name_seq=None):
    result = ''
    type_ = None

    reverse_name_dict = {}
    name_count = 0

    for k, v in name_dict.items():
        reverse_name_dict[v] = k

    for token in tokens.split():
        try:
            prev_type_was_op = (type_ == 'op')

            type_, content = token.split('>_')
            type_ = type_.lstrip('_<')

            if type_ == 'id':
                if name_seq is not None:
                    content = name_seq[name_count]
                    name_count += 1
                else:
                    try:
                        content = reverse_name_dict[content.rstrip('@')]
                    except KeyError:
                        content = 'new_id_' + content.rstrip('@')
            elif type_ == 'number':
                content = content.rstrip('#')

            if type_ == 'directive' or type_ == 'include' or type_ == 'op' or type_ == 'type' or type_ == 'keyword' or type_ == 'APIcall'or type_ == 'pa':
                if type_ == 'op' and prev_type_was_op:
                    result = result[:-1] + content + ' '
                else:
                    result += content + ' '
            elif type_ == 'id':
                result += content + ' '
            elif type_ == 'number':
                result += '0 '
            elif type_ == 'string':
                result += '"String" '
            elif type_ == 'char':
                result += "'c' "
        except ValueError:
            if token == '~':
                result += '\n'

    if not clang_format:
        return result


def prepare_date_strs_padded(date_strs):
    

    
    X = prepare_data(date_strs)
    
    if X.shape[1] < max_input_length:
        X = tf.pad(X, [[0, 0], [0, max_input_length - X.shape[1]]])
    return X



def predict_date_strs(date_strs):
    
    X = prepare_date_strs_padded(date_strs)
    print(X)
    
    Y_pred = tf.fill(dims=(len(X), 1), value=sos_id)
    #print(Y_pred)
    for index in range(max_output_length):
        pad_size = max_output_length - Y_pred.shape[1]
        X_decoder = tf.pad(Y_pred, [[0, 0], [0, pad_size]])
        Y_probas_next = model.predict([X, X_decoder])[:, index:index+1]
        #print(Y_probas_next)
        #print(Y_probas_next[:, index:index+1])
        Y_pred_next = tf.argmax(Y_probas_next, axis=-1, output_type=tf.int32)
        #print(Y_pred_next)
        Y_pred = tf.concat([Y_pred, Y_pred_next], axis=1)
        #print(Y_pred)
    print(Y_pred[:, 1:])

    tokens = ids_to_token(Y_pred[:, 1:].numpy())[0]
    print(tokens)
    strs = tokens_to_source(tokens,INPUT_CHARS)
    
    return strs



if __name__ == '__main__':
   

    checkpoint_path = "training_token/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    #print(latest)

    model = create_model()
    model.load_weights(latest)
    
    df = pd.read_csv('../data/printf_autocreate.csv')
    
    X_train, Y_train = create_dataset(df['wrong'][0:70000], df['correct'][0:70000])
    X_valid, Y_valid = create_dataset(df['wrong'][70000:100000], df['correct'][70000:100000])
    

    
    max_input_length = X_train.shape[1]
    max_output_length = Y_train.shape[1]


    
    filename = "c1.c"
    folder_path = f'{filename}'
    

    warning_text = run_compiler(folder_path)

    column = find_column(warning_text, filename)
    file_data = ""
    line_column = 1
    with open(folder_path, "r") as f:

        for line in f:
            if str(line_column) in column:
                printf_positions = [m.span()
                                    for m in regex.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    
                    
                    model = create_model()
                    model.load_weights(latest)
                    print("model input: "+line[printf_positions[0][0]:])
                    wrong_str = line[printf_positions[0][0]:]
                    print(wrong_str)
                    print("printf(\" %lf %lf %lf\", jk, FXF, LdP),")
                    print(wrong_str.strip() == "printf(\" %lf %lf %lf\", jk, FXF, LdP),")
                    
                    tokenized_code, name_dict, name_seq = tokenize( "printf(\" %lf %lf %lf\", jk, FXF, LdP),")
                    print(tokenized_code, name_dict, name_seq)
                    
                    fixed_str = predict_date_strs("printf(\" %lf %lf %lf\", jk, FXF, LdP),")
                    print("model output: "+fixed_str)
                   

            file_data += line

            line_column = line_column+1
        #print(file_data)