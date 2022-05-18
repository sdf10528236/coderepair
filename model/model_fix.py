import regex
import pandas as pd
import string
import tensorflow as tf 

import os
from model.model_test import create_model,run_compiler,find_column,create_dataset,predict_date_strs


INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=\n\() ,;.\"[]%'!&"
sos_id = len(OUTPUT_CHARS) + 1


df = pd.read_csv('/home/laz/Program/coderepair/data/printf_autocreate.csv')


X_train, Y_train = create_dataset(df['wrong'][0:80000], df['correct'][0:80000])
X_valid, Y_valid = create_dataset(df['wrong'][80000:100000], df['correct'][80000:100000])



max_input_length = X_train.shape[1]
max_output_length = Y_train.shape[1]





def column_fix(old_file, new_file, column):
    line_column = 1
    file_data = ""
    checkpoint_path = "/home/laz/Program/coderepair/model/training_autocreate_2l/cp-{epoch:04d}.ckpt"
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
                    print(line[printf_positions[0][0]:])
                    wrong_str = line[printf_positions[0][0]:]
                    try:
                        fix_line = predict_date_strs([wrong_str])[0]
                        #print(fix_line)
                    

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