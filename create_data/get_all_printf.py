import os
import numpy as np
import pandas as pd
import regex
from auto_corrupt_syntax import auto_corrupt_syntax, auto_corrupt_printf
import random
import string


def printf_add_word(cur_line_str):
    WORDS = ("python", "good", "easy", "difficult", "Hello world!", "hello")
    word = random.choice(WORDS)
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    
    to_corrupt = positions[0]  # 第一個"的地方
    cur_line_str = cur_line_str[:to_corrupt[0]+1]+word+cur_line_str[to_corrupt[0]+1:]
    print(cur_line_str)
    return cur_line_str


def printf_add_parameter(cur_line_str, numbers):
    #format_placeholder = ["d", "f", "s", "c"]
    format_placeholder = ["d"]

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]]

    for i in range(numbers):
        cur_line_str = cur_line_str + \
            " %" + format_placeholder[0]

    cur_line_str = cur_line_str + "\""
    for i in range(numbers):
        cur_line_str = cur_line_str + ", "+"".join(random.choice(
            string.ascii_letters.lower())) 
    cur_line_str = cur_line_str + ");"
    print(cur_line_str)
    return cur_line_str


def creat_printf(numbers, number_of_strings=10):  # 產生printf("字串")程式碼
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters.lower())
                                                for _ in range(random.randint(0, number_of_strings)))+"\");")

    return cur_line_str

def find_printf(cur_line_str):
    printf_position_list = []

    printf_positions = [m.span()for m in regex.finditer(
        'printf', cur_line_str)]  # 找到printf字串位置
    end_positions = [m.span()for m in regex.finditer(
        ';', cur_line_str)]  # 找到printf行 ; 的位置
    printf_positions = list(printf_positions)

    for printf_position in printf_positions:
        end_position = min((i[1] for i in end_positions if i[1] >
                            printf_position[0]), key=lambda x: abs(x - printf_position[0]))

        printf_position = (printf_position[0], end_position)
        printf_position_list.append(printf_position)

    return printf_position_list


if __name__ == '__main__':

    folder_path = '/home/laz/Program/coderepair/data/codinghere_data/'
    folderList = os.listdir(folder_path)
    folderList.sort()
    #print(folderList)
    cnt = 0
    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)
    cur_line_strs = []

    for base in folderList:
        path = folder_path + base + "/" + "correct"
        fileList = os.listdir(path)
        fileList.sort()
        for file in fileList:
            filepath = path + "/" + file
            #print(filepath)
            f = open(filepath)
            try:
                cur_line_strs.append(f.read())
                print(len(cur_line_strs))
            except:
                continue
    #-----------------------------------------------------------------------------------------------------------------------------
    # for cur_line_str in cur_line_strs:

    #     printf_position_list = find_printf(cur_line_str)
    #     # print(printf_position_list)
    #     for (start, end) in printf_position_list:
    #         if(end-start) > 50:
    #             continue
    #         else:
    #             special01 = [m.span()for m in regex.finditer(
    #                 'for', cur_line_str[start:end])]
    #             special02 = [m.span()for m in regex.finditer(
    #                 'No', cur_line_str[start:end])]
    #             if(len(special01) == 0 and len(special02) == 0):
    #                 cur_line_str_correct = cur_line_str[start:end]
    #                 #print(cur_line_str_correct)
    #             else:
    #                 continue

    #         for i in range(random.randint(5, 20)):
    #             cur_line_str_wrong = cur_line_str_correct
    #             for i in range(random.randint(1, 3)):
    #                 cur_line_str_wrong = auto_corrupt_syntax(
    #                     cur_line_str_wrong)
    #             corrupt_printf = np.random.choice(
    #                 2, p=[0.6, 0.4])  # 依照概率選擇是否corrupt_printf字串
    #             if corrupt_printf:
    #                 cur_line_str_wrong = auto_corrupt_printf(
    #                     cur_line_str_wrong)

    #             df = df.append({
    #                 "correct": cur_line_str_correct,
    #                 "wrong": cur_line_str_wrong,
    #             }, ignore_index=True)
    #             print(cnt)
    #             cnt = cnt+1

    #----------------------------------------------------------------------------------------
    cur_line_strs = creat_printf(2000, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter(
            cur_line_strs[i], random.randint(0, 4))    #printf("%d",a);
    for cur_line_str in cur_line_strs:
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 20)):
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
    cur_line_strs = creat_printf(20, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_word(          #printf("hello");
            cur_line_strs[i])
    for cur_line_str in cur_line_strs:
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 20)):
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
    cur_line_strs = creat_printf(2000)               #printf("sdfsdgqw");
    
    for cur_line_str in cur_line_strs:
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 20)):
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





    #print(df)
    #df = df.sample(frac=1).reset_index(drop = True)
    print(df)
    df.to_csv("../data/printf03.csv",
             encoding='utf-8', index=False)
