import os
import numpy as np
import pandas as pd
import regex


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

    folder_path = 'D:/program projects/coderepair/data/codinghere_data/'
    folderList = os.listdir(folder_path)

    cnt = 0
    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)
    cur_line_str = []

    for base in folderList[:1]:
        path = folder_path + base + "/" + "correct"
        fileList = os.listdir(path)
        for file in fileList[:1]:
            filepath = path + "/" + file
            f = open(filepath)
            cur_line_str.append(f.read())
    for cur_line_str in cur_line_str:

        printf_position_list = find_printf(cur_line_str)

        print(printf_position_list)

        positions = printf_position_list[np.random.randint(
            len(printf_position_list))]
        print(positions)
        to_corrupt = cur_line_str[positions[0]:positions[1]]
        print(to_corrupt)
        # print(positions)

    # --------------------寫入csv-----------------------------
    # for cur_line_str in cur_line_str:

    #     df = df.append({
    #         "correct": cur_line_str,
    #         "wrong": cur_line_str,
    #     }, ignore_index=True)
    #     cnt = cnt+1
    #     print("now is ", cnt, "data")

    # print(df)
    # df.to_csv("../data/codinghere_correct_test.csv",
    #           encoding='utf-8', index=False)
