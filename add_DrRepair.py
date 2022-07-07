import argparse
import os
import subprocess
import shutil
import json, base64, os
import urllib.parse
from model.eval_model import EvalModel
import time


modelpath = "model/training_token_printfnew"




def create_folder(path):    #創建資料夾，不論原本有沒有此資料夾，都會重新創建一個
    
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)

def get_dir_files(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-1:]=='c']
    files.sort()
    return files

def write_to_file(filepath, code):
        with open(filepath, 'w') as f:
            f.write(code) 

def run_code_fix(args): #filepath, compiler_path="gcc"):
    
    if args.file:               #若輸入為檔案
       print("請輸入資料夾")
            
        
        
        
        
    elif args.idir:    #若輸入為資料夾
        start = time.time()
        print("Program start...")
        em = EvalModel(modelpath)    
        for file in get_dir_files(args.idir):
            
            copy_file = 'copy.c'
            copy_path = 'data'
            code_copy_path = os.path.join(copy_path ,copy_file)
            Dr_copy_path = 'data/DrRepair.c'
            os.system(f"cp {args.idir}/{file} {code_copy_path}")    #將原檔案複製一份到data/copy.c 供coderepair修復, 避免修復過程更動到原檔案
            #shutil.copyfile(f'{args.idir}/{file}',os.path.join(copy_path ,copy_file)) 
            os.system(f"cp {args.idir}/{file} {Dr_copy_path}")  #將原檔案複製一份到data/DrRepair.c 供DrRepair修復, 避免修復過程更動到原檔案
            #shutil.copyfile(f'{args.idir}/{file}','data/DrRepair.c') 
            print("filename:"+file)

            for i in range(5):
                
                DrRepair_fix(Dr_copy_path) #跑DrRepair 模型,跑完結果在 data/DrRepair.c 
        
                em.coderepair_fix_file(code_copy_path) #跑coderepair 模型,跑完結果在 data/copy.c 
 
                DrRepair_len = len(compile_file(Dr_copy_path))       
                coderepair_len = len(compile_file(code_copy_path))
                if (i>=4):#若修復五次
                    os.system(f"cp {code_copy_path} {fail_fix_folder}/co_{file}")
                    os.system(f"cp {Dr_copy_path} {fail_fix_folder}/Dr_{file}")
                    #shutil.copyfile(os.path.join(copy_path ,copy_file) ,f'{fail_fix_folder}/co_{file}')
                    #shutil.copyfile('data/DrRepair.c',f'{fail_fix_folder}/Dr_{file}')
                    print("try over 5 times! fix error! move it to error data!") 
                    break
                elif (DrRepair_len > coderepair_len):     #coderepair 修復後錯誤訊息較少
                    if coderepair_len:           
                        with open(code_copy_path, "r") as f:
                            coderepair_code = f.read()
                        write_to_file(Dr_copy_path,coderepair_code)                     #將DrRepair.c 檔內容 用copy.c 檔內容取代
                    else:
                        os.system(f"cp {code_copy_path} {sucees_fix_folder}/{file}") #coderepair 修復後無錯誤訊息,表示修復成功
                        #shutil.copyfile(os.path.join(copy_path ,copy_file),f'{sucees_fix_folder}/{file}')
                        print("coderepair compiled!")                             
                        break
                elif(coderepair_len > DrRepair_len):    #DrRepair 修復後錯誤訊息較少
                    if DrRepair_len:
                        with open(Dr_copy_path, "r") as f:
                            DrRepair_code = f.read()
                        write_to_file(code_copy_path,DrRepair_code)                             #將copy.c 檔內容 用DrRepair.c 檔內容取代
                    else:
                        #shutil.copyfile('data/DrRepair.c',f'{sucees_fix_folder}/{file}')
                        os.system(f"cp {Dr_copy_path} {sucees_fix_folder}/{file}")
                        print("DrRepair compiled!")                             #DrRepair 修復後無錯誤訊息,表示修復成功
                        break
                elif(coderepair_len == 0 and DrRepair_len == 0):
                    #coderepair，DrRepair 修復後皆無錯誤訊息
                    #修復結果複製到two_sucees_folder資料夾
                    #shutil.copyfile(os.path.join(copy_path ,copy_file),f'{two_sucees_folder}/co_{file}') 
                    #shutil.copyfile('data/DrRepair.c',f'{two_sucees_folder}/Dr_{file}')
                    os.system(f"cp {code_copy_path} {two_sucees_folder}/co_{file}")
                    os.system(f"cp {Dr_copy_path} {two_sucees_folder}/Dr_{file}")
                    print("two compiled!")
                    break
                else:
                    #coderepair，DrRepair 修復後錯誤訊息長度相同，則繼續迭代
                    print("two compiled len same")


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
    
    two_sucees_folder = 'data/two_mix_sucess'
    sucees_fix_folder = 'data/mix_sucess'
    fail_fix_folder = 'data/mix_fail'
    
    create_folder(two_sucees_folder) #創建資料夾，不論原本有沒有此資料夾，都會重新創建一個
    create_folder(sucees_fix_folder)
    create_folder(fail_fix_folder)


    parser = argparse.ArgumentParser(description='fix printf error code files by using model')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    
    run_code_fix(opts)
    
    
