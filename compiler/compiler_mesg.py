from difflib import SequenceMatcher
import subprocess
import pandas as pd
import argparse
import regex
import os
import shutil


def get_dir_files(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-1:]=='c']
    files.sort()
    return files

def compile_file(file):
    p = subprocess.run(['gcc', file], capture_output=True)
    result = p.stderr.decode("utf-8").splitlines()
    return result

def run_compiler(args): #filepath, compiler_path="gcc"):
    print(args.idir)
    if args.file:
        result = compile_file(args.file)
        print(result)
        
    elif args.idir:
        for file in get_dir_files(args.idir):
            print(file)
            result = compile_file(os.path.join(args.idir, file))
            print (result)
            column = find_column(result,file)
            find_printf_line(os.path.join(args.idir, file),column)
            


def find_printf_line(file,column):
    print(column)
    line_column = 1
    
    with open(file, "r") as f:

        for line in f:
            if str(line_column) in column:
                printf_positions = [m.span()
                                    for m in regex.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    
                   
                    
                    fix_line = line[printf_positions[0][0]:]
                    print(fix_line)

                    check_printf_error(fix_line)

            

            line_column = line_column+1
        #print(file_data)
            
def check_printf_error(line):
    file_data ='''
        #include <stdio.h>
        int main()
        {
            
        
        '''+f"{line}"+'''    return 0;
        }'''


    print(file_data)
    file_name = "test/temp.c"
    with open(file_name, "w") as f:
        f.write(file_data)
    result = compile_file(file_name)
    for text in result:
        error_p = [m.span()for m in regex.finditer('error', text)]
        warning_p = [m.span()for m in regex.finditer('warning', text)]
        if(len(error_p ) or len(warning_p)):
            undeclared_p = [m.span()
                               for m in regex.finditer("undeclared", text)]
            if(len(undeclared_p)):
                print(text)
            else:
                print("!!!!!!!!!!!!!!!!!!!!")
                print(text)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
              

        

             
        
            
def find_column(warning_text, filename):
    column = []
    for text in warning_text:
        print(text)
        error_p = [m.span()for m in regex.finditer('error', text)]
        warning_p = [m.span()for m in regex.finditer('warning', text)]
        if(len(error_p ) or len(warning_p)):
            # print(text)
            colon_positions = [m.span()
                               for m in regex.finditer(":", text)]  # 冒號位置
            colume_start = [m.span()
                            for m in regex.finditer(f"{filename}:", text)]
            
            if(len(colon_positions) and len(colume_start)):
                column_end = min((i[0] for i in colon_positions if i[0] >
                              colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))
                new_line = text[colume_start[0][1]:column_end]
                if new_line not in column:

                    column.append(new_line) 
            

    return column
   


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check files by using compiler')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    run_compiler(opts)

