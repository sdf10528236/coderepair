import random
import string
import random
import regex
import pandas as pd
import numpy as np
from auto_corrupt_syntax import auto_corrupt_syntax

def creat_printf(numbers, number_of_strings=20):  # 產生printf("字串")程式碼    ex. printf("sdfsdgqw");
    cur_line_str = []
    for i in range(numbers):
        cur_line_str.append("printf(\""+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(0, number_of_strings)))+"\");")

    return cur_line_str

def printf_parameter_string(cur_line_str, numbers):  # ex. printf("asdasd %d %d ", a, b);
    format_placeholder = ["d", "f","lf"]
    choice = ['0','1']
    format_placeholder = random.choice(format_placeholder)
   
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]]

    for i in range(numbers):
        if int(random.choices(choice)[0]):
            cur_line_str = cur_line_str+" "+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(0, 10)))
        cur_line_str = cur_line_str + \
            " %" + format_placeholder
        if int(random.choices(choice)[0]):
            cur_line_str = cur_line_str+" "+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(0, 10)))
       
        

    cur_line_str = cur_line_str + "\""
    for i in range(numbers):
        cur_line_str = cur_line_str + ", "+"".join(random.choice(
            string.ascii_letters)for _ in range(random.randint(1, 3)))
    cur_line_str = cur_line_str + ");"

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方
    for i in range(random.randint(0,1)):
        cur_line_str = cur_line_str[:to_corrupt[0]]+"\\n"+cur_line_str[to_corrupt[0]:]
    print(cur_line_str)
    return cur_line_str

def printf_add_parameter(cur_line_str, numbers):  # ex. printf("%d",a);
    format_placeholder = ["d", "f", "s", "c","lf"]
    
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
            string.ascii_letters)for _ in range(random.randint(1, 3)))
    cur_line_str = cur_line_str + ");"


    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方
    for i in range(random.randint(0,1)):
        cur_line_str = cur_line_str[:to_corrupt[0]]+"\\n"+cur_line_str[to_corrupt[0]:]
    print(cur_line_str)
    return cur_line_str

def printf_add_parameter_op(cur_line_str, numbers):  # ex. #printf(" %d %d", p/x, V+GMp-H/x);
    format_placeholder = ["d", "f","lf"]
    op = ["+","-","*","/"]
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
        cur_line_str = cur_line_str + ", "
        
        if random.randint(0,1):
            cur_line_str = cur_line_str+"".join(random.choice(
                string.ascii_letters)for _ in range(random.randint(1, 3)))
        else:
            cur_line_str = cur_line_str+"".join(str(random.randint(1, 20)))
        
        for i in range(1):
            cur_line_str = cur_line_str+"".join(random.choice(
            op))
        if random.randint(0,1):
            cur_line_str = cur_line_str+"".join(random.choice(
                string.ascii_letters)for _ in range(random.randint(1, 3)))
        else:
            cur_line_str = cur_line_str+"".join(str(random.randint(1, 20)))
    
    cur_line_str = cur_line_str + ");"
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方
    for i in range(random.randint(0,1)):
        cur_line_str = cur_line_str[:to_corrupt[0]]+"\\n"+cur_line_str[to_corrupt[0]:]

    print(cur_line_str)
    return cur_line_str





def printf_string(cur_line_str, numbers):  # 產生printf("字串 字串 字串");    ex. printf("sdfsdgqw sdf sdfsdf");
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]] + " "

    for i in range(numbers):
        cur_line_str = cur_line_str+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(0, 10)))+" "
    cur_line_str = cur_line_str + "\");"

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方
    for i in range(random.randint(0,1)):
        cur_line_str = cur_line_str[:to_corrupt[0]]+"\\n"+cur_line_str[to_corrupt[0]:]
    print(cur_line_str)
    return cur_line_str




    
if __name__ == '__main__':
    cnt = 1
    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)

    #--------------------------------------------------------------------------------------------
    cur_line_strs = []
    cur_line_strs = creat_printf(5000, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter(
            cur_line_strs[i], random.randint(1, 5))    #printf(" %d %d %d", wPX, v, NIn);
    for cur_line_str in cur_line_strs:
        
        
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 10)):
            cur_line_str_wrong = cur_line_str_correct
            for i in range(random.randint(1, 2)):
                cur_line_str_wrong = auto_corrupt_syntax(
                    cur_line_str_wrong)
            

            df = df.append({
                "correct": cur_line_str_correct,
                "wrong": cur_line_str_wrong,
            }, ignore_index=True)
            print(cnt)
            cnt = cnt+1

    #--------------------------------------------------------------------------------------------
    cur_line_strs = []
    cur_line_strs = creat_printf(5000, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_parameter_string(
            cur_line_strs[i], random.randint(1, 5))    #printf("asdasd %d %d ", a, b);
    for cur_line_str in cur_line_strs:
        
        
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 10)):
            cur_line_str_wrong = cur_line_str_correct
            for i in range(random.randint(1, 2)):
                cur_line_str_wrong = auto_corrupt_syntax(
                    cur_line_str_wrong)
            

            df = df.append({
                "correct": cur_line_str_correct,
                "wrong": cur_line_str_wrong,
            }, ignore_index=True)
            print(cnt)
            cnt = cnt+1
    #--------------------------------------------------------------------------------------------


    #--------------------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------------------------------------------
    cur_line_strs = creat_printf(2500)               #printf("ZldxM YTQr Kdt JxoSjTm\n");
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_string(
            cur_line_strs[i], random.randint(0, 5))
    for cur_line_str in cur_line_strs:
        
        cur_line_str_correct = cur_line_str
        for i in range(random.randint(5, 10)):
            cur_line_str_wrong = cur_line_str_correct
            for i in range(random.randint(1, 2)):
                cur_line_str_wrong = auto_corrupt_syntax(cur_line_str_wrong)
          

            df = df.append({
                "correct": cur_line_str_correct,
                "wrong": cur_line_str_wrong,
            }, ignore_index=True)
            print(cnt)
            cnt = cnt+1

    #--------------------------------------------------------------------------------------------------------------------
    df = df.sample(frac=1).reset_index(drop = True)
    print(df)
    df.to_csv("../data/printf_new2.csv",
             encoding='utf-8', index=False)

