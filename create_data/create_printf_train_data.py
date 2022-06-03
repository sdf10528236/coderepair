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

def printf_parameter_string(cur_line_str, numbers):  # ex. printf("%d + asd %d ", a, b);
    format_placeholder = ["d", "f","lf"]
    
    format_placeholder = random.choice(format_placeholder)
    op = ["+","-","*","="]
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]]

    for i in range(numbers):
        cur_line_str = cur_line_str + \
            " %" + format_placeholder
        if i < numbers-1: 
            for i in range(random.randint(0,1)):
                cur_line_str = cur_line_str+ " "+"".join(random.choice(
            op))
            for i in range(random.randint(0,1)):
                if random.randint(0,1):
                    cur_line_str = cur_line_str+" "+"".join(random.choice(
                    string.ascii_letters)for _ in range(random.randint(1, 3)))
                else:
                    cur_line_str = cur_line_str+" "+"".join(str(random.randint(1, 20)))
        

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



def printf_add_op(cur_line_str):  # ex.  printf("Pokah*123+WDM*f-Tt\n");
    op = ["+","-","*","/","="]
    cur_line_str = "printf(\"\");"
    #------------------
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    to_corrupt = positions[1]  # 第2個"的地方
    cur_line_str = cur_line_str[:to_corrupt[0]]+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(1, 10)))+cur_line_str[to_corrupt[0]:]
    #------------------                                            
    
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    to_corrupt = positions[1]  # 第2個"的地方
    cur_line_str = cur_line_str[:to_corrupt[0]]
    for i in range(random.randint(0,5)):
        if random.randint(0,1):
            cur_line_str = cur_line_str+" "+"".join(random.choice(
                op))
        if random.randint(0,1):
            cur_line_str = cur_line_str+" "+"".join(random.choice(
                string.ascii_letters)for _ in range(random.randint(1, 3)))
        else:
            cur_line_str = cur_line_str+" "+"".join(str(random.randint(1, 20)))
            
    cur_line_str = cur_line_str+"\");"
    #------------------

    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方
    for i in range(random.randint(0,1)):
        cur_line_str = cur_line_str[:to_corrupt[0]]+"\\n"+cur_line_str[to_corrupt[0]:]
    print(cur_line_str)
    return cur_line_str 

def printf_string(cur_line_str, numbers):  # 產生printf("字串 字串 字串")程式碼    ex. printf("sdfsdgqw sdf sdfsdf");
    positions = [m.span()
                 for m in regex.finditer("\"", cur_line_str)]
    # print(cur_line_str, positions)
    to_corrupt = positions[1]  # 第二個"的地方

    cur_line_str = cur_line_str[:to_corrupt[0]]

    for i in range(random.randint(0,numbers)):
        cur_line_str = cur_line_str+" "+"".join(random.choice(string.ascii_letters)
                                                for _ in range(random.randint(0, 10)))
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
    cur_line_strs = creat_printf(5, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter(
            cur_line_strs[i], random.randint(1, 3))    #printf(" %d %d %d", wPX, v, NIn);
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
    cur_line_strs = creat_printf(5, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_parameter_string(
            cur_line_strs[i], random.randint(1, 4))    #printf(" %d %d + %d", mof, U, vNv);
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
    cur_line_strs = creat_printf(5, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_parameter_op(
            cur_line_strs[i], random.randint(1, 3))    #printf(" %d %d", p/33, V+GMp-H/x);
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
    cur_line_strs = creat_printf(5, 0)
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_add_op(          #printf("Ugnj / 10 m = iDj * 4\n");
            cur_line_strs[i])
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
    #--------------------------------------------------------------------------------------------------------------------
    cur_line_strs = creat_printf(5)               #printf("ZldxM YTQr Kdt JxoSjTm\n");
    for i in range(len(cur_line_strs)):
        cur_line_strs[i] = printf_string(
            cur_line_strs[i], random.randint(1, 5))
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
    df.to_csv("../data/printf_test.csv",
             encoding='utf-8', index=False)

