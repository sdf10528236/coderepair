import numbers
import string
import random
import regex


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
            string.ascii_letters)) + "["+"".join(random.choice(
                string.ascii_letters)) + "]"

    cur_line_str = cur_line_str + ");"
    print(cur_line_str)
    return cur_line_str


def creat_printf(numbers, number_of_strings=10):  # 產生printf("字串")程式碼
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(0, number_of_strings)))+"\");")

    return cur_line_str


if __name__ == '__main__':

    cur_line_strs = creat_printf(10, 0)
    print(len(cur_line_strs))
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter(
            cur_line_strs[i], random.randint(1, 2))

    print(cur_line_strs)
