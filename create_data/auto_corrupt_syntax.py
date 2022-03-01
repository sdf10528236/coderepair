import os
import numpy as np
import regex
import string
import random
import pandas as pd
DEBUG_MODE = 0  # 1 (除錯用)


def creat_scanf(numbers, parameter_number=4, number_of_strings=4):  # 產生printf("字串")程式碼
    cur_line_str = []

    for i in range(numbers):
        cur_line_str.append("scanf(\""+"\");")
        cur_line_str[i] = scanf_add_parameter(
            cur_line_str[i], parameter_number, number_of_strings)

    print(cur_line_str)
    return cur_line_str


def scanf_add_parameter(cur_line_str, parameter_number, number_of_strings):
    format_placeholder = ["d", "f", "s", "c"]
    temporary_str = ""
    parameter_number = random.randint(1, parameter_number)
    temporary_str = "".join(" %"+format_placeholder[random.randint(0, 3)]
                            for _ in range(parameter_number))
    temporary_str = temporary_str + "\","
    temporary_str = temporary_str + "".join((" &" + "".join(random.choice(string.ascii_letters)
                                                            for _ in range(number_of_strings)))for _ in range(parameter_number))

    positions = [m.span()for m in regex.finditer("\"", cur_line_str)]
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]] + temporary_str\
        + cur_line_str[to_corrupt[1]:]
    return cur_line_str


def creat_printf(numbers, number_of_strings=10):  # 產生printf("字串")程式碼
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(1, number_of_strings)))+"\");")
        cur_line_str[i] = printf_add_parameter(cur_line_str[i])

    return cur_line_str


def printf_add_parameter(cur_line_str):
    format_placeholder = ["d", "f", "s", "c"]

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]] + \
        " = %" + format_placeholder[random.randint(0, 3)] + "\", " + "".join(random.choice(string.ascii_letters)
                                                                             for _ in range(random.randint(1, 4))) + cur_line_str[to_corrupt[1]:]
    print(cur_line_str)
    return cur_line_str


def auto_corrupt_scanf(cur_line_str):
    try:
        positions = [m.span()for m in regex.finditer(
            'scanf', cur_line_str)]  # 找到scanf字串位置
        to_corrupt = np.random.choice(
            positions[0][1]-positions[0][0], p=[0.05, 0.1, 0.1, 0.1, 0.65])  # 依照p概率選擇要刪除scanff當中的某字元

        cur_line_str = cur_line_str[:to_corrupt] + cur_line_str[to_corrupt+1:]

        return cur_line_str

    except:
        return cur_line_str


def find_scanf(cur_line_str):
    scanf_position_list = []

    scanf_positions = [m.span()for m in regex.finditer(
        'scanf', cur_line_str)]  # 找到printf字串位置
    end_positions = [m.span()for m in regex.finditer(
        ';', cur_line_str)]  # 找到printf行 ; 的位置

    for scanf_position in scanf_positions:
        end_position = min((i[1] for i in end_positions if i[1] >
                            scanf_position[0]), key=lambda x: abs(x - scanf_position[0]))

        scanf_position = (scanf_position[0], end_position)
        scanf_position_list.append(scanf_position)

    return scanf_position_list


def find_printf(cur_line_str):
    printf_position_list = []

    printf_positions = [m.span()for m in regex.finditer(
        'printf', cur_line_str)]  # 找到printf字串位置
    end_positions = [m.span()for m in regex.finditer(
        ';', cur_line_str)]  # 找到printf行 ; 的位置

    for printf_position in printf_positions:
        end_position = min((i[1] for i in end_positions if i[1] >
                            printf_position[0]), key=lambda x: abs(x - printf_position[0]))

        printf_position = (printf_position[0], end_position)
        printf_position_list.append(printf_position)

    return printf_position_list


def auto_corrupt_printf(cur_line_str):

    positions = [m.span()for m in regex.finditer(
        'printf', cur_line_str)]  # 找到printf字串位置
    if(len(positions) > 0):
        printf_position = positions[np.random.randint(
            len(positions))]  # 隨機選取printf行首字位置

        to_corrupt = np.random.choice(
            printf_position[1]-printf_position[0], p=[0.03, 0.08, 0.08, 0.08, 0.08, 0.65])  # 依照p概率選擇要刪除printf當中的某字元

        cur_line_str = cur_line_str[:to_corrupt] + cur_line_str[to_corrupt+1:]
        # print(cur_line_str)
        return cur_line_str
    else:
        return cur_line_str


def auto_corrupt_kw_typo(cur_line_str):
    actions = {0: auto_corrupt_printf, 1: auto_corrupt_scanf}
    cur_line_str = actions[np.random.randint(0, 2)](
        cur_line_str)  # 隨機選擇actions
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

        if DEBUG_MODE:  # 除錯用
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

            cur_line_str = cur_line_str[:positions[to_corrupt][0]] + \
                _patt[1] + cur_line_str[positions[to_corrupt][1]:]

            # print(cur_line_str)
    return cur_line_str


if __name__ == '__main__':
    folder_path = 'D:/program projects/coderepair/data/codinghere_data/'
    folderList = os.listdir(folder_path)
    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)
    cnt = 0
    cur_line_str = []
    printf_position_list = []
    scanf_position_list = []

    for base in folderList:
        path = folder_path + base + "/" + "correct"
        fileList = os.listdir(path)
        for file in fileList:
            filepath = path + "/" + file
            f = open(filepath)
            try:
                cur_line_str.append(f.read())
            except:
                cur_line_str = cur_line_str

    actions = {0: auto_corrupt_syntax,
               1: auto_corrupt_kw_typo}

    for cur_line_str in cur_line_str:

        printf_position_list = find_printf(cur_line_str)
        scanf_position_list = find_scanf(cur_line_str)

        cur_line_str_wrong = cur_line_str
        for i in range(10):

            if(len(printf_position_list) == 0):
                break

            number = np.random.randint(
                len(printf_position_list))  # 隨機選擇一筆定位數據
            positions = printf_position_list[number]

            to_corrupt = cur_line_str_wrong[positions[0]:positions[1]]

            corrupt = actions[np.random.randint(0, 2)](
                to_corrupt)  # 隨機選擇actions

            cur_line_str_wrong = cur_line_str_wrong[:positions[0]
                                                    ]+corrupt+cur_line_str_wrong[positions[1]:]

            if (len(corrupt) != len(to_corrupt)):  # 若該行定位已跟原本不同,則在printf_position_list中刪除該行資訊,避免定位失準
                if number == len(printf_position_list):
                    printf_position_list = printf_position_list[:number]
                else:
                    printf_position_list = printf_position_list[:number] + \
                        printf_position_list[number+1:]

        for i in range(10):

            if(len(scanf_position_list) == 0):
                break

            number = np.random.randint(
                len(scanf_position_list))  # 隨機選擇一筆定位數據
            positions = scanf_position_list[number]
            print(positions)
            to_corrupt = cur_line_str_wrong[positions[0]:positions[1]]

            corrupt = actions[np.random.randint(0, 2)](
                to_corrupt)  # 隨機選擇actions

            cur_line_str_wrong = cur_line_str_wrong[:positions[0]
                                                    ]+corrupt+cur_line_str_wrong[positions[1]:]

            if (len(corrupt) != len(to_corrupt)):  # 若該行定位已跟原本不同,則在printf_position_list中刪除該行資訊,避免定位失準
                if number == len(scanf_position_list):
                    scanf_position_list = scanf_position_list[:number]
                else:
                    scanf_position_list = scanf_position_list[:number] + \
                        scanf_position_list[number+1:]

        df = df.append({
            "correct": cur_line_str,
            "wrong": cur_line_str_wrong,
        }, ignore_index=True)

        cnt = cnt+1
        #print("now is ", cnt, "data")
        # print(cur_line_str)

    print(df)
    df.to_csv("../data/test.csv",
              encoding='utf-8', index=False)
