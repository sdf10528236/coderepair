import imp
import pandas as pd
from util.c_tokenizer import C_Tokenizer
import re as regex
import os
import shutil
tokenize = C_Tokenizer().tokenize

def get_parament(data):
    
    tokenized_code, name_dict, name_seq,pa_dict,pa_sequence = tokenize(data)
    print(pa_sequence )
    return pa_sequence
        
def get_var(data):
    var_list = []
    print(data)
    p = [m.span()for m in regex.finditer(",", data)]
    d = [m.span()for m in regex.finditer("\)", data)]
    print(p)
    print(d)
    num = len(p)
    if num:
        for i in range(num):
            if i+1 < num:
                var = data[p[i][1]:p[i+1][0]]   
                var_list.append(var)
                print(var)
            else:
                var = data[p[i][1]:d[0][0]]
                var_list.append(var)
                print(var)

    print(var_list)
    return var_list

def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        print("fold already exit")
   



if __name__ == '__main__':
    df = pd.read_csv('data/printf_new.csv')

   
    number = 1
    folder_num = 1
    for data in df['correct']:
        if number%10000 == 1:
            folder = f'data/DrRepair_train_data/porb{folder_num}/correct'
            create_folder(folder)
            folder_num+=1
        print(data)
       
        pa_list = get_parament(data)
        var_list = get_var(data)

        code1 = '''#include <stdio.h>
#include <string.h>

int main()
{

'''

        code2 = '''
    return 0;
}
'''
        if not os.path.isfile(f"{folder}/{number}.c"):
            os.mknod(f"{folder}/{number}.c")

        with open(f"{folder}/{number}.c", "w") as f:
            all_code = code1
            lens = len(pa_list)
            if lens > 0:
                for i in range(lens):
                    if pa_list[i] == "%d":
                        all_code+="\t"+"int "+ var_list[i]+";\n"
                    elif pa_list[i] == "%f":
                        all_code+="\t"+"float "+ var_list[i]+";\n"
                    elif pa_list[i] == "%lf":
                        all_code+="\t"+"double "+ var_list[i]+";\n"
                    elif pa_list[i] == "%c":
                        all_code+="\t"+"char "+ var_list[i]+";\n"    
                    elif pa_list[i] == "%s":
                        all_code+="\t"+"char "+ var_list[i]+"[100]"+";\n" 
            all_code+="\t"+data
            all_code+=code2
            f.write(all_code)
        number+=1


