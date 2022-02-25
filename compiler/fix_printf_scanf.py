import os
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex


def str_warning(warning_text):
    printf_fix_line = {}
    scanf_fix_line = {}
    for text in warning_text:

        p = [m.span()for m in regex.finditer('\'', text)]

        if len(p) != 0:
            for i in range(len(p)):

                if i % 2 == 0:
                    position_start = p[i][1]
                else:
                    position_end = p[i][0]
                    string = text[position_start:position_end]
                    if SequenceMatcher(None, "printf", string).ratio() > 0.7:
                        column = [m.span()
                                  for m in regex.finditer(":", text)]

                        column_line = text[column[0][1]:column[1][0]]

                        if column_line not in printf_fix_line:

                            printf_fix_line[column_line] = string

                    elif SequenceMatcher(None, "scanf", string).ratio() > 0.7:
                        column = [m.span()
                                  for m in regex.finditer(":", text)]

                        column_line = text[column[0][1]:column[1][0]]

                        # print(text)
                        if column_line not in scanf_fix_line:

                            scanf_fix_line[column_line] = string

    return printf_fix_line, scanf_fix_line


if __name__ == '__main__':

    file_path = 'D:/program projects/coderepair/data/wrong_data/'
    fileList = os.listdir(file_path)
    for file in fileList:
        filename = file

        p = subprocess.run(
            ["D:/Program Files/CodeBlocks/MinGW/bin/gcc.exe", f"../data/wrong_data/{filename}"], capture_output=True)
        print(p.stderr.decode("utf-8"))
        warning_text = p.stderr.decode("utf-8").splitlines()
        printf_fix_line, scanf_fix_line = str_warning(warning_text)

        line_column = 1
        file_data = ""
        with open(f"../data/wrong_data/{filename}", "r") as f:

            for line in f:
                if str(line_column) in printf_fix_line:
                    line = line.replace(
                        printf_fix_line[str(line_column)], "printf")
                elif str(line_column) in scanf_fix_line:
                    line = line.replace(
                        scanf_fix_line[str(line_column)], "scanf")
                file_data += line

                line_column = line_column+1
        with open(f"../data/correct_data/c{filename}", "w") as f:
            f.write(file_data)
        line_column = 1
