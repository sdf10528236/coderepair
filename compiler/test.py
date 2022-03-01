
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex
if __name__ == '__main__':
    filename = "c1.c"
    folder_path = f'D:/program projects/coderepair/data/correct_data/{filename}'

    p = subprocess.run(
        ["D:/Program Files/CodeBlocks/MinGW/bin/gcc.exe", folder_path], capture_output=True)
    print(p.stderr.decode("utf-8"))
