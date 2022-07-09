import argparse
import os
import subprocess
import shutil
import os
import tensorflow as tf
import json, base64, os
import urllib.parse




def create_folder(path):        #創建資料夾，不論原本有沒有此資料夾，都會重新創建一個
    
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
    
    if args.file:     #若輸入為檔案
        print("請輸入資料夾")
        
        
        
        
    elif args.idir:      #若輸入為資料夾
            
        for file in get_dir_files(args.idir):
            
            copy_file = 'onlyDrRepair.c'
            copy_path = 'data'
            err_file = os.path.join(copy_path ,copy_file)
            shutil.copyfile(f'{args.idir}/{file}',err_file) #將原檔案複製一份到data/onlyDrRepair.c 供DrRepair修復, 避免修復過程更動到原檔案
            print("filename:"+file)   
            DrRepair_fix(err_file)    #跑DrRepair 模型,跑完結果在 data/onlyDrRepair.c 檔 

            DrRepair_len = len(compile_file(err_file))       
                
            if DrRepair_len:
                #DrRepair 修復後還有錯誤訊息
                shutil.copyfile(err_file,f'{fail_fix_folder}/{file}')
                print("DrRepair fail!") 
                
            else:
                shutil.copyfile(err_file,f'{sucees_fix_folder}/{file}')
                #DrRepair 修復後無錯誤訊息
                print("DrRepair compiled!")
                
                
                
                   


def compile_file(file):
    p = subprocess.run(['gcc', file], capture_output=True)
    #print(p.stderr.decode("utf-8"))
    result = p.stderr.decode("utf-8").splitlines()
    return result
            

def DrRepair_fix(file):
    with open(file, "r") as f:
        code = f.read()
    
    data = {
        "probid": 'test001', # this.problem.id,
        "info": "INFO",
        "subid": "Subid",
        "code": code,
    }

    datastr = json.dumps(data) #.replace("'", "\\'")
    msg = base64.b64encode(datastr.encode())
    umsg = urllib.parse.quote(msg)
    command = f"curl http://140.135.13.120:3000/test3388/pred3389?q={umsg}"
    ans = os.popen(command).read()
    
    with open(file, 'w') as f:
        f.write(ans)
    

if __name__ == '__main__':
    
 
    sucees_fix_folder = 'data/Dr_sucess'
    fail_fix_folder = 'data/Dr_fail'
    
    
    create_folder(sucees_fix_folder)    #創建資料夾，不論原本有沒有此資料夾，都會重新創建一個
    create_folder(fail_fix_folder)


    parser = argparse.ArgumentParser(description='fix  code files by DrRepair model')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    
    run_code_fix(opts)
    