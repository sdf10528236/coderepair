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
        check_printf(result)
    elif args.idir:
        for file in get_dir_files(args.idir):
            print(file)
            result = compile_file(os.path.join(args.idir, file))
            print("  ", result)
            if check_printf(result):
                shutil.copyfile(f"{args.idir}/{file}",f"pwdata/{file}")


def check_printf(result):
    check = 1 
    for text in result:
        #print(text)
        if check:
            mean_position = printf_positions = [m.span()
                            for m in regex.finditer('mean', text)]
            printf_positions = [m.span()
                            for m in regex.finditer('printf', text)]
            ismean = len (mean_position)
            isprintf = len(printf_positions)
            if isprintf:
                if ismean:
                    print("i find it !!!!!!!!")
                    return 1
                else:
                    check = 0 
        else:
            p_up = text.find('^')
            if p_up >= printf_positions[0][0]:
                check = 1
                print("i find it !!!!!!!!")
                return 1
            else:
                check =1  
            
            
   


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check files by using compiler')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    run_compiler(opts)

