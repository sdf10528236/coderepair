import argparse
import os
import shutil
from model.eval_model import EvalModel
import time

modelpath = "model/training_token_printfnew"

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)

def get_dir_files(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-1:]=='c']
    files.sort()
    return files

def run_code_fix(args): #filepath, compiler_path="gcc"):
    if args.file:
        print("please input folder")
        
    elif args.idir:
        start = time.time()
        print("Program start...")
        em = EvalModel(modelpath)
        input_path = 'data/input_data'          
        if not os.path.isdir(input_path):
            os.mkdir(input_path)
        else:
            shutil.rmtree(input_path)
            os.mkdir(input_path)
        #創建一個input_data資料夾                                     

        os.system(f"cp {args.idir}/*.c {input_path}/")
        # for file in get_dir_files(args.idir):
        #     shutil.copyfile(f'{args.idir}/{file}',f'{input_path}/{file}')
        #將原輸入的資料複製一份到input_data資料夾
        success, total = 0, 0
        for file in get_dir_files(input_path):
            success += em.try_fix_file(input_path, file)
            total += 1

        end = time.time()
        print(f"\nFinished! Spent time = {end-start:.2f}s")
        print(f"Total = {total}, Success = {success}, Rate = {success/total:.2f}")

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
    
    
