import os
import numpy as np
import pandas as pd
import regex


if __name__ == '__main__':

    data = pd.read_csv("../data/test.csv")
    cur_line_str = []
    filename = 1
    for data in data['wrong'][:10]:

        with open(f"../data/wrong_data/{filename}.c", "w") as f:
            f.write(data)
        filename = filename + 1
