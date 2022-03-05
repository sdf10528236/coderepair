import regex
from difflib import SequenceMatcher
import subprocess
import pandas as pd
from model_test.model01 import create_model, predict_date_strs
import os
folder = os.path.dirname(os.path.abspath(__file__))
latest = f'{folder}/cp.ckpt'

def run_compiler(filepath, compiler_path="gcc"):
    p = subprocess.run(
        [compiler_path, filepath], capture_output=True)

    warning_text = p.stderr.decode("utf-8").splitlines()
    return warning_text


def column_fix(old_file, new_file, column):
    line_column = 1
    file_data = ""
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


if __name__ == '__main__':
   
    filename = "c1.c"
    folder_path = f'../data/correct_data/{filename}'
    auto_model_fix(folder_path, filename)
