
from turtle import position
import numpy as np

import pandas as pd


if __name__ == '__main__':
    basename = "CodeTest"
    df = pd.read_csv('../data/test.csv')
    srcname = basename + ".c"
    outfile = open(srcname, 'w')
    outfile.write(df['wrong'][1])
    outfile.close()
