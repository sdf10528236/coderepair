import random
import string
import random
import regex
def printf_add_word(cur_line_str):
    WORDS = ("python", "good", "easy", "difficult", "Hello world!", "hello")
    word = random.choice(WORDS)
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    
    to_corrupt = positions[0]  # 第一個"的地方
    cur_line_str = cur_line_str[:to_corrupt[0]+1]+"\""+word+cur_line_str[to_corrupt[0]+1:]
    print(cur_line_str)


def printf_add_parameter(cur_line_str, numbers):
    format_placeholder = ["d", "f", "s", "c"]
    

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]]

    for i in range(numbers):
        cur_line_str = cur_line_str + \
            " %" + random.choice(format_placeholder)

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


if __name__ == '__main__':

    cur_line_strs = creat_printf(100, 0)
    print(len(cur_line_strs))
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter(
            cur_line_strs[i], random.randint(1, 4))
        
        # cur_line_strs[i] = printf_add_word(
        #     cur_line_strs[i])
    print(cur_line_strs)
