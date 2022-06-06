#import regex
import pandas as pd
import string
import tensorflow as tf 
import subprocess
import os
import numpy as np
from model.model_train import create_model
import re as regex
from util.c_tokenizer import C_Tokenizer
tokenize = C_Tokenizer().tokenize

now_path = os.path.dirname(os.path.abspath(__file__))
INPUT_CHARS = np.load(now_path+'/all_dicts.npy',allow_pickle=True).item()
OUTPUT_CHARS = np.load(now_path+'/all_dicts.npy',allow_pickle=True).item()
id_to_token_dict = {v:k for k,v in INPUT_CHARS.items()}

sos_id = len(OUTPUT_CHARS) + 1



def data_str_to_token(data_str):
    #print(data_str)
    tokenized_code, name_dict, name_seq,pa_dict,pa_sequence = tokenize(data_str)
   
    tokenized_code_list = tokenized_code.split()
    
        
    tokenized_code_list=[]
    #print(tokenized_code.split())
    for token in tokenized_code.split():
        
        if '_<id>_' in token:
            
            token = '_<id>_@'
         
        if '_<pa>_' in token:
            
            token = '_<pa>_@'
            
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



def tokens_to_source(tokens, name_dict, clang_format=False, name_seq=None,pa_seq = None):
    result = ''
    type_ = None

    reverse_name_dict = {}
    name_count = 0
    pa_count = 0


    for k, v in name_dict.items():
        reverse_name_dict[v] = k

    for token in tokens.split():
        try:
            prev_type_was_op = (type_ == 'op')

            type_, content = token.split('>_')
            type_ = type_.lstrip('_<')

            if type_ == 'id':
                if name_seq is not None:
                    
                    if(name_count > (len(name_seq)-1)):   #預測出來的<id>數量大於原本name_seq裡的<id>數
                        name_count = (len(name_seq)-1)
                    try:
                        content = name_seq[name_count]
                    except:
                        content = ""
                    name_count += 1
                else:
                    try:
                        content = reverse_name_dict[content.rstrip('@')]
                    except KeyError:
                        content = 'new_id_' + content.rstrip('@')
            elif type_ == 'pa':
                if pa_seq is not None:
                    
                    if(pa_count > (len(pa_seq)-1)):   #預測出來的<id>數量大於原本name_seq裡的<id>數
                        pa_count = (len(pa_seq)-1)
                    try:
                        content = pa_seq[pa_count]
                    except:
                        content = ""
                    pa_count += 1
                else:
                    try:
                        content = reverse_name_dict[content.rstrip('@')]
                    except KeyError:
                        content = 'new_id_' + content.rstrip('@')
            elif type_ == 'number':
                content = content.rstrip('#')

            if type_ == 'directive' or type_ == 'include' or type_ == 'op' or type_ == 'type' or type_ == 'keyword' or type_ == 'APIcall':
                if type_ == 'op' and prev_type_was_op:
                    result = result[:-1] + content + ' '
                else:
                    result += content + ' '
            elif type_ == 'es':
               
                result = result[:-1] + content[1:] + ' '   #新增/n /t

            elif type_ == 'id':
                result += content + ' '
            elif type_ == 'pa':
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



def predict_date_strs(date_strs,model):
    
    X = prepare_date_strs_padded(date_strs)
    #print(X)
    
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
    #print(Y_pred[:, 1:])

    tokens = ids_to_token(Y_pred[:, 1:].numpy())[0]
    #print(tokens)
    tokenized_code, name_dict, name_seq = tokenize(date_strs)
    strs = tokens_to_source(tokens,INPUT_CHARS,False,name_seq)
    
    return strs


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
        w = [m.span()for m in regex.finditer('warning', text)]
        if(len(p) > 0 or len(w)>0):
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


def column_fix(old_file, new_file, column, model):
    global total
    line_column = 1
    file_data = ""

    with open(old_file, "r") as f:

        for line in f:
            if str(line_column) in column:
                printf_positions = [m.span()
                                    for m in regex.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    wrong_str = line[printf_positions[0][0]:]

                    print("model input: "+wrong_str)
                    try:
                        fix_line = predict_date_strs(wrong_str.strip(),model)
                        
                        
                        print("model output: "+fix_line)
                        

                        line = line[:printf_positions[0][0]] + \
                        fix_line + "\n"
                    except:
                        line = line
                        #print(INPUT_CHARS)
            file_data += line

            line_column = line_column+1
        # print(file_data)
    with open(new_file, "w") as f:
        f.write(file_data)





def auto_model_fix(folder_path, new_folder,filename,model):
    
    warning_text = run_compiler(folder_path)

    column = find_column(warning_text, filename)
    column_fix(folder_path, new_folder, column, model)
    
df = pd.read_csv(f'{os.getcwd()}/data/printf_new.csv')
X_train, Y_train = create_dataset(df['wrong'][0:125000], df['correct'][0:125000])
X_valid, Y_valid = create_dataset(df['wrong'][125000:180000], df['correct'][125000:180000])
    

max_input_length = X_train.shape[1]
max_output_length = Y_train.shape[1]



if __name__ == '__main__':
   

   
    
    filename = "c1.c"
    folder_path = f'{filename}'
    

    auto_model_fix(folder_path,"c1fix.c","c1.c")