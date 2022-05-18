import regex
import pandas as pd
import string
import tensorflow as tf 
import subprocess
import os
import numpy as np
from model.model_train import create_model,predict_date_strs,create_dataset


INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"
sos_id = len(OUTPUT_CHARS) + 1

df = pd.read_csv(f'{os.getcwd()}/data/printf_autocreate.csv')
X_train, Y_train = create_dataset(df['wrong'][0:80000], df['correct'][0:80000])
X_valid, Y_valid = create_dataset(df['wrong'][80000:100000], df['correct'][80000:100000])
    

max_input_length = X_train.shape[1]
max_output_length = Y_train.shape[1]


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




   



def predict_date_strs(date_strs,model):
    
    X = prepare_date_strs_padded(date_strs)
    Y_pred = tf.fill(dims=(len(X), 1), value=sos_id)
    for index in range(max_output_length):
        pad_size = max_output_length - Y_pred.shape[1]
        X_decoder = tf.pad(Y_pred, [[0, 0], [0, pad_size]])
        Y_probas_next = model.predict([X, X_decoder])[:, index:index+1]
        Y_pred_next = tf.argmax(Y_probas_next, axis=-1, output_type=tf.int32)
        Y_pred = tf.concat([Y_pred, Y_pred_next], axis=1)
    return ids_to_date_strs(Y_pred[:, 1:])



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

def column_fix(old_file, new_file, column):
    line_column = 1
    file_data = ""
    checkpoint_path = "/home/laz/Program/coderepair/model/training_autocreate_Bidirectional/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    with open(old_file, "r") as f:

        for line in f:
            if str(line_column) in column:
                printf_positions = [m.span()
                                    for m in regex.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    
                    
                    model = create_model()
                    model.load_weights(latest)
                    
                    wrong_str = line[printf_positions[0][0]:]

                    print("model input: "+wrong_str)
                    try:
                        fix_line = predict_date_strs([wrong_str],model)[0]
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





def auto_model_fix(folder_path, new_folder,filename):
    warning_text = run_compiler(folder_path)

    column = find_column(warning_text, filename)
    column_fix(folder_path, new_folder, column)
    




if __name__ == '__main__':
   

   
    
    filename = "c1.c"
    folder_path = f'{filename}'
    

    auto_model_fix(folder_path,"c1fix.c","c1.c")