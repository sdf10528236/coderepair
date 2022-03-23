import random
import string
import random
import regex
import pandas as pd
import numpy as np
from auto_corrupt_syntax import auto_corrupt_syntax, auto_corrupt_printf

def printf_add_word(cur_line_str):
    WORDS = ("python", "good", "difficult", "Hello world!", "hello", "nice", "Yes", "No", "Error", "I can do it!", "\n", "This and this are the same string in Python.")
    word = random.choice(WORDS)
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    
    to_corrupt = positions[0]  # 第一個"的地方
    cur_line_str = cur_line_str[:to_corrupt[0]+1]+word+cur_line_str[to_corrupt[0]+1:]
    print(cur_line_str)
    return cur_line_str


def printf_add_parameter(cur_line_str, numbers):
    format_placeholder = ["d", "f", "s", "c"]
    format_placeholder = random.choice(format_placeholder)

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]]

    for i in range(numbers):
        cur_line_str = cur_line_str + \
            " %" + format_placeholder

    cur_line_str = cur_line_str + "\""
    for i in range(numbers):
        cur_line_str = cur_line_str + ", "+"".join(random.choice(
            string.ascii_letters.lower()) for _ in range(random.randint(0, 3))) 
    cur_line_str = cur_line_str + ");"
    print(cur_line_str)
    return cur_line_str


def creat_printf(numbers, number_of_strings=10):  # 產生printf("字串")程式碼
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters.lower())
                                                for _ in range(random.randint(0, number_of_strings)))+"\");")

    return cur_line_str



if __name__ == '__main__':
    cnt = 1
    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)
    cur_line_strs = []
    cur_line_strs = creat_printf(2000, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter(
            cur_line_strs[i], random.randint(1, 3))    #printf("%d",a);
    for cur_line_str in cur_line_strs:
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 10)):
            cur_line_str_wrong = cur_line_str_correct
            for i in range(random.randint(1, 2)):
                cur_line_str_wrong = auto_corrupt_syntax(
                    cur_line_str_wrong)
            corrupt_printf = np.random.choice(
                2, p=[0.6, 0.4])  # 依照概率選擇是否corrupt_printf字串
            if corrupt_printf:
                cur_line_str_wrong = auto_corrupt_printf(
                    cur_line_str_wrong)

            df = df.append({
                "correct": cur_line_str_correct,
                "wrong": cur_line_str_wrong,
            }, ignore_index=True)
            print(cnt)
            cnt = cnt+1


    #--------------------------------------------------------------------------------------------
    cur_line_strs = creat_printf(30, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_word(          #printf("hello");
            cur_line_strs[i])
    for cur_line_str in cur_line_strs:
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 10)):
            cur_line_str_wrong = cur_line_str_correct
            for i in range(random.randint(1, 2)):
                cur_line_str_wrong = auto_corrupt_syntax(
                    cur_line_str_wrong)
            corrupt_printf = np.random.choice(
                2, p=[0.6, 0.4])  # 依照概率選擇是否corrupt_printf字串
            if corrupt_printf:
                cur_line_str_wrong = auto_corrupt_printf(
                    cur_line_str_wrong)

            df = df.append({
                "correct": cur_line_str_correct,
                "wrong": cur_line_str_wrong,
            }, ignore_index=True)
            print(cnt)
            cnt = cnt+1
    #--------------------------------------------------------------------------------------------------------------------
    cur_line_strs = creat_printf(2500)               #printf("sdfsdgqw");
    
    for cur_line_str in cur_line_strs:
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 10)):
            cur_line_str_wrong = cur_line_str_correct
            for i in range(random.randint(1, 2)):
                cur_line_str_wrong = auto_corrupt_syntax(
                    cur_line_str_wrong)
            corrupt_printf = np.random.choice(
                2, p=[0.6, 0.4])  # 依照概率選擇是否corrupt_printf字串
            if corrupt_printf:
                cur_line_str_wrong = auto_corrupt_printf(
                    cur_line_str_wrong)

            df = df.append({
                "correct": cur_line_str_correct,
                "wrong": cur_line_str_wrong,
            }, ignore_index=True)
            print(cnt)
            cnt = cnt+1

    #--------------------------------------------------------------------------------------------------------------------

    print(df)
    df.to_csv("../data/printf_autocreate.csv",
             encoding='utf-8', index=False)

