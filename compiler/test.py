
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex
if __name__ == '__main__':
    filename = "c1.c"
    folder_path = f'../data/correct_data/{filename}'

    p = subprocess.run(
        ["gcc", folder_path], capture_output=True)
    print(p.stderr.decode("utf-8"))
