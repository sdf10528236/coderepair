import os
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex


def fix_str(old_file, new_file, printf_fix_line, scanf_fix_line):
    line_column = 1
    file_data = ""
    with open(old_file, "r") as f:

        for line in f:
            if str(line_column) in printf_fix_line:
                line = line.replace(
                    printf_fix_line[str(line_column)], "printf")
            elif str(line_column) in scanf_fix_line:
                line = line.replace(
                    scanf_fix_line[str(line_column)], "scanf")
            file_data += line

            line_column = line_column+1
    with open(new_file, "w") as f:
        f.write(file_data)


def run_compiler(path):
    p = subprocess.run(
        ["gcc", path], capture_output=True)
    # print(p.stderr.decode("utf-8"))
    warning_text = p.stderr.decode("utf-8").splitlines()
    #print(p.stderr.decode("utf-8"))
    return warning_text


def str_warning(filename, warning_text):
    printf_fix_line = {}
    scanf_fix_line = {}
    for text in warning_text:
        text = text.replace("‘","\'")
        text = text.replace("’","\'")
        p = [m.span()for m in regex.finditer("\'", text)]
        
        if len(p) != 0:
            for i in range(len(p)):

                if i % 2 == 0:
                    position_start = p[i][1]
                else:
                    position_end = p[i][0]
                    string = text[position_start:position_end]
                    
                    
                    if SequenceMatcher(None, "printf", string).ratio() > 0.7:
                        colon_positions = [m.span()
                                           for m in regex.finditer(":", text)]  # 冒號位置
                        colume_start = [m.span()
                                        for m in regex.finditer(f"{filename}:", text)]
                        column_end = min((i[0] for i in colon_positions if i[0] >
                                          colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))

                        column_line = text[colume_start[0][1]:column_end]

                        if column_line not in printf_fix_line:

                            printf_fix_line[column_line] = string

                    elif SequenceMatcher(None, "scanf", string).ratio() > 0.7:
                        colon_positions = [m.span()
                                           for m in regex.finditer(":", text)]  # 冒號位置
                        colume_start = [m.span()
                                        for m in regex.finditer(f"{filename}:", text)]
                        column_end = min((i[0] for i in colon_positions if i[0] >
                                          colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))

                        column_line = text[colume_start[0][1]:column_end]

                        # print(text)
                        if column_line not in scanf_fix_line:

                            scanf_fix_line[column_line] = string

    return printf_fix_line, scanf_fix_line


def auto_fix_str(file_path, filename):
    warning_text = run_compiler(file_path)

    printf_fix_line, scanf_fix_line = str_warning(filename, warning_text)

    fix_str(file_path,
            file_path, printf_fix_line, scanf_fix_line)


if __name__ == '__main__':
    filename = 'c1.c'
    folder_path = f'../data/correct_data/{filename}'

    auto_fix_str(folder_path, filename)

    
