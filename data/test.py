from turtle import position
import numpy as np
import regex
import re
import string
import random
import pandas as pd


def creat_printf(numbers, number_of_strings):
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(1, number_of_strings)))+"\");")

    return cur_line_str


if __name__ == '__main__':

    print(np.random.choice(5, p=[0.34, 0.15, 0.2, 0.3, 0.01]))
