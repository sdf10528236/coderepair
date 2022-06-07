import os
import numpy as np
import regex
import string
import random
import pandas as pd
DEBUG_MODE = 0  # 1 (除錯用)


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
        'duplicate,': (",", ",,"), 
        'duplicate"': ("\"", "\"\""),        
        'duplicate{': ("\{", "{ {"),
        'duplicate}': ("\}", "} }"),
        'duplicate[': ("\[", "[ ["),
        'duplicate]': ("\]", "] ]"),
        'replace;with,': (";", ","),
        'replace;with.': (";", "."),
        'replace;with:': (";", ":"),
        'replace\"with\'': ("\"", "\'"),
        'replace\\n\"with\"\\n': (r"\\n\"", "\"\\n"), 
        'replace);with");': ("\);", "\");"),
        
        'replace);with;)': ("\) ;", "; )"),
    }

    #'duplicate(': ("\(", "( ("),
    #'duplicate)': ("\)", ") )"),
    #'duplicate,': (",", ", ,"),
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
    print("auto_corrupt_syntax")
