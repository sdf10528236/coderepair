from str_fix.fix_printf_scanf import auto_fix_str
from model.model_fix import auto_model_fix
import argparse
import os
import subprocess
import shutil
import os



def create_folder(path):
    
    if not os.path.isdir(path):
        os.mkdir(path)


def get_dir_files(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-1:]=='c']
    files.sort()
    return files

def run_code_fix(args): #filepath, compiler_path="gcc"):
    
    if args.file:
        print("please input folder")
        
        
    elif args.idir:
        input_path = 'data/input_data'          
        if not os.path.isdir(input_path):
            os.mkdir(input_path)
        else:
            shutil.rmtree(input_path)
            os.mkdir(input_path)
        #創建一個input_data資料夾                                     

        for file in get_dir_files(args.idir):
            
            shutil.copyfile(f'{args.idir}/{file}',f'{input_path}/{file}')
        #將原輸入的資料複製一份到input_data資料夾
               
        for file in get_dir_files(input_path):
            print("filename:"+file)
            for i in range(5):
                
                if(code_fix(os.path.join(input_path, file),file)==1):
                    
                    shutil.copyfile(f'{input_path}/{file}',f'{sucees_fix_folder}/{file}')
                    print("move to success folder")
                    break
                elif(code_fix(os.path.join(input_path, file),file)==2):
                    shutil.copyfile(f'{input_path}/{file}',f'{fail_fix_folder}/{file}')
                    print("model output error ! fix error! move it to error data!") 
                    break
                elif (i == 4):  #若修復五次
                    shutil.copyfile(f'{input_path}/{file}',f'{fail_fix_folder}/{file}')
                    print("try over 5 times! fix error! move it to error data!")  
        #程式修復流程


def compile_file(file):
    p = subprocess.run(['gcc', file], capture_output=True)
    #print(p.stderr.decode("utf-8"))
    result = p.stderr.decode("utf-8").splitlines()
    return result
            
def code_fix(file_path,filename):
    if (len(compile_file(file_path))):
        

        auto_fix_str(file_path,file_path,filename)
    

        if (len(compile_file(file_path))):
            error_num = len(compile_file(file_path))
            auto_model_fix(file_path,file_path,filename)
            if (len(compile_file(file_path))== error_num):
                return 2
            elif (len(compile_file(file_path))):
                return 0
            else:
                print("code fix success!")
                return 1
        else:
            print("code fix success!")
            return 1

    else:
        print("code fix success!")
        return 1

if __name__ == '__main__':
    
    sucees_fix_folder = 'data/sucess'
    fail_fix_folder = 'data/fail'
    
    create_folder(sucees_fix_folder)
    create_folder(fail_fix_folder)


    parser = argparse.ArgumentParser(description='fix printf error code files by using model')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    
    run_code_fix(opts)
    
    
