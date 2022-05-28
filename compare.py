import numpy as np
import pandas as pd
import string
import os

INPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=~@#$^|\n\t`{}\\() ,;.\"[]%'!&?"

OUTPUT_CHARS = "".join(
    sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=~@#$^|\n\t`{}\\() ,;.\"[]%'!&?"
    
sos_id = len(OUTPUT_CHARS) + 1


def data_str_to_ids(date_str, chars):
    return [1+chars.index(c) for c in date_str]

def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    print(X_ids)
    xlen = max(len(x) for x in X_ids)
    y = []
    for i in range(len(X_ids)):
        y.append(X_ids[i] + [0]*(xlen-len(X_ids[i])))
    print(np.array(y))
    return np.array(y)

def create_dataset(x, y):
    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)

if __name__ == '__main__':
    df = pd.read_csv('data/printf_autocreate.csv')
    X_train, Y_train = create_dataset(df['wrong'][0:10], df['correct'][0:10])
    