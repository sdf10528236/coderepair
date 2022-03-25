from compiler.fix_printf_scanf import auto_fix_str
from model_test.model_fix import auto_model_fix
#from compiler.compile_msg import run_compiler
import argparse
import os
import subprocess
import shutil

def get_dir_files(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-1:]=='c']
    files.sort()
    return files

def run_code_fix(args): #filepath, compiler_path="gcc"):
    
    if args.file:
        print(args.file)
        
        
    elif args.idir:
        for file in get_dir_files(args.idir):
            print(file)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            for i in range(10):
                if(code_fix(os.path.join(args.idir, file),file)):
                    shutil.copyfile(f'{args.idir}/{file}',f'data/fsdata/{file}')
                    print("move to success folder")
                    break
                elif (i == 9):
                    shutil.copyfile(f'{args.idir}/{file}',f'data/ffdata/{file}')
                    print("fix error! move it to error data!")  
                


def compile_file(file):
    p = subprocess.run(['gcc', file], capture_output=True)
    result = p.stderr.decode("utf-8").splitlines()
    return result
            
def code_fix(file_path,filename):
    if (len(compile_file(file_path))):

        auto_fix_str(file_path,file_path,filename)
    

        if (len(compile_file(file_path))):
            auto_model_fix(file_path,file_path,filename)
            return 0
        else:
            print("code fix success!")
            return 1

    else:
        print("code fix success!")
        return 1

if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(description='fix printf error code files by using model')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    
    run_code_fix(opts)
    
