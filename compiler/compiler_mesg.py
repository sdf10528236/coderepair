import regex
from difflib import SequenceMatcher
import subprocess
import pandas as pd

import os


def run_compiler(filepath, compiler_path="gcc"):
    p = subprocess.run(
        [compiler_path, filepath], capture_output=True)

    warning_text = p.stderr.decode("utf-8").splitlines()
    return warning_text


if __name__ == '__main__':

    filename = "c1.c"
    folder_path = f'D:/program projects/coderepair/data/correct_data/{filename}'
   
    warning_text = run_compiler(folder_path)
