from turtle import position
import numpy as np
import regex
import re
import string
import random
import pandas as pd
DEBUG_MODE = 0  # 1


def creat_printf(numbers, number_of_strings):
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(1, number_of_strings)))+"\");")

    return cur_line_str


def auto_corrupt_printf(cur_line_str):

    positions = [m.span()for m in regex.finditer(
        '^printf', cur_line_str)]  # 找到首位printf字串

    to_corrupt = np.random.choice(
        positions[0][1]-positions[0][0], p=[0.1, 0.15, 0.15, 0.15, 0.15, 0.3])  # 依照p概率選擇要刪除printf當中的某字元

    cur_line_str = cur_line_str[:to_corrupt] + cur_line_str[to_corrupt+1:]
    return cur_line_str


def auto_corrupt_syntax(cur_line_str):

    __action_pattern_map = {
        'delete"': ("\"", ""),
        'delete(': ("\(", ""),
        'delete)': ("\)", ""),
        'delete,': (",", ""),
        'delete;': (";", ""),
        'delete{': ("\{", ""),
        'delete}': ("\}", ""),
        'delete[': ("\[", ""),
        'delete]': ("\]", ""),
        'delete+': ("\+", ""),
        'delete-': ("-", ""),
        'delete=': ("=", ""),
        'delete<': ("<", ""),
        'delete>': (">", ""),
        'delete>': ("&", ""),
        'delete>': ("\*", ""),
        'duplicate(': ("\(", "( ("),
        'duplicate)': ("\)", ") )"),
        'duplicate,': (",", ", ,"),
        'duplicate{': ("\{", "{ {"),
        'duplicate}': ("\}", "} }"),
        'duplicate[': ("\[", "[ ["),
        'duplicate]': ("\]", "] ]"),
        'replace;with,': (";", ","),
        'replace,with;': (",", ";"),
        'replace;with.': (";", "."),
        'replace);with;)': ("\) ;", "; )"),
    }
    _actions = list(__action_pattern_map.keys())

    positions = {}
    while(len(positions) == 0):
        _action = _actions[np.random.randint(
            len(_actions))]  # 隨機選擇__actions
        if DEBUG_MODE:
            print("action picked:", _action)
        _patt = __action_pattern_map[_action]

        positions = [m.span()
                     for m in regex.finditer(_patt[0], cur_line_str)]

        if len(positions) == 0:
            _action = _actions[np.random.randint(len(_actions))]
        else:
            if len(positions) > 1:
                to_corrupt = np.random.randint(len(positions))
            else:
                to_corrupt = 0
            # print("")
            # print(cur_line_str)
            # print(_patt)
            # print(_patt[0])

            # print(positions)

            cur_line_str = cur_line_str[:positions[to_corrupt][0]] + \
                _patt[1] + cur_line_str[positions[to_corrupt][1]:]

            # print(cur_line_str)
    return cur_line_str


if __name__ == '__main__':

    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)

    numbers = 1000

    cur_line_str = creat_printf(numbers, 20)

    actions = {0: auto_corrupt_printf, 1: auto_corrupt_syntax}

    for cur_line_str in cur_line_str:
        # print(cur_line_str)

        cur_line_str_wrong = actions[np.random.randint(0, 2)](
            cur_line_str)  # 隨機選擇actions
        df = df.append({
            "correct": cur_line_str,
            "wrong": cur_line_str_wrong,
        }, ignore_index=True)
        # print(cur_line_str)

    print(df)
    df.to_csv("../data/printf_test.csv", encoding='utf-8', index=False)
