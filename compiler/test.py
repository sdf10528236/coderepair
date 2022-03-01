
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex
if __name__ == '__main__':

    folder_path = 'D:/program projects/coderepair/data/codinghere_data/BASE001/erroneous/c-0b7PJJ-80575p.c'
    df = pd.read_csv('../data/test.csv')
    filename = "c1.c"
    p = subprocess.run(
        ["D:/Program Files/CodeBlocks/MinGW/bin/gcc.exe", filename], capture_output=True)
    print(p.stderr.decode("utf-8"))
