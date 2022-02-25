import imp
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex
if __name__ == '__main__':
    folder_path = 'D:/program projects/coderepair/data/codinghere_data/BASE001/erroneous/c-0b7PJJ-80575p.c'
    df = pd.read_csv('../data/test.csv')
    filename = "CodeTest.c"
    p = subprocess.run(
        ["D:/Program Files/CodeBlocks/MinGW/bin/gcc.exe", filename], capture_output=True)
    print(p.stderr.decode("utf-8"))
    warning_text = p.stderr.decode("utf-8").splitlines()

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

                        # print(text)
                        if text[len(filename)+1:len(filename)+2] not in printf_fix_line:

                            printf_fix_line[text[len(
                                filename)+1:len(filename)+2]] = string

                    elif SequenceMatcher(None, "scanf", string).ratio() > 0.7:

                        # print(text)
                        if text[len(filename)+1:len(filename)+2] not in scanf_fix_line:

                            scanf_fix_line[text[len(
                                filename)+1:len(filename)+2]] = string

    #print(printf_fix_line, scanf_fix_line)
    line_column = 1
    file_data = ""
    with open(filename, "r") as f:

        for line in f:
            if str(line_column) in printf_fix_line:
                line = line.replace(
                    printf_fix_line[str(line_column)], "printf")
            elif str(line_column) in scanf_fix_line:
                line = line.replace(
                    scanf_fix_line[str(line_column)], "scanf")
            file_data += line

            line_column = line_column+1
    with open(filename, "w") as f:
        f.write(file_data)
    line_column = 1
