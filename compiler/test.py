
import pandas as pd
import subprocess
from difflib import SequenceMatcher
import regex
if __name__ == '__main__':

    filename = "CodeTest"

    line_column = 1
    file_data = ""
    with open(f"{filename}.c", "r") as f:

        for line in f:
            print(line.split())
            file_data += line

            line_column = line_column+1

    line_column = 1
