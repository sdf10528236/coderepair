from str_fix.fix_printf_scanf import auto_fix_str
from model.model_fix import auto_model_fix
from model.model_train import create_model
import argparse
import os
import subprocess
import shutil
import os
import tensorflow as tf
import json, base64, os
import urllib.parse


now_path = os.path.dirname(os.path.abspath(__file__))
checkpoint_path = now_path+"/model/training_token_printfnew/cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
#print(latest)

model = create_model()
model.load_weights(latest)

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
        code = ""
        copy_file = 'copy.c'
        copy_path = 'data'
        shutil.copyfile(f'{args.file}',os.path.join(copy_path ,copy_file)) #將原檔案複製一份到copy.c
        

        for i in range(5):
            if(i == 0 ):
                DrRepair_fix(args.file)   #跑DrRepair 模型,跑完結果在 data資料夾 裡的 DrRepair.c 檔 
            else:
                DrRepair_fix('data/DrRepair.c')
            for j in range(5):
                with open(os.path.join(copy_path ,copy_file), "r") as f:
                    old_code = f.read()
                code_fix(os.path.join(copy_path ,copy_file) ,copy_file)  #跑coderepair 模型,跑完結果在 data資料夾 裡的 copy.c 檔 
                with open(os.path.join(copy_path ,copy_file), "r") as f:
                        new_code = f.read()
                if old_code.split() == new_code.split():
                    break
            DrRepair_len = len(compile_file('data/DrRepair.c'))       
            coderepair_len = len(compile_file(os.path.join(copy_path ,copy_file)))
            if (i>=4):#若修復五次
                shutil.copyfile(os.path.join(copy_path ,copy_file) ,f'{fail_fix_folder}/co_{args.file}')
                shutil.copyfile('data/DrRepair.c',f'{fail_fix_folder}/Dr_{args.file}')
                print("try over 5 times! fix error! move it to error data!") 
                break
            elif (DrRepair_len > coderepair_len):     #coderepair 修復後錯誤訊息較少
                if coderepair_len:           
                    with open(os.path.join(copy_path ,copy_file), "r") as f:
                        coderepair = f.read()
                    with open('data/DrRepair.c', 'w') as f:
                        f.write(coderepair)                        #將DrRepair.c 檔內容 用copy.c 檔內容取代
                else:
                    shutil.copyfile(os.path.join(copy_path ,copy_file),f'{sucees_fix_folder}/{args.file}')
                    print("coderepair compiled!")                             #coderepair 修復後無錯誤訊息
                    break
            elif(coderepair_len > DrRepair_len):    #DrRepair 修復後錯誤訊息較少
                if DrRepair_len:
                    with open('data/DrRepair.c', "r") as f:
                        DrRepair = f.read()
                    with open(os.path.join(copy_path ,copy_file), "w") as f:
                        f.write(DrRepair)                           #將copy.c 檔內容 用DrRepair.c 檔內容取代
                else:
                    shutil.copyfile('data/DrRepair.c',f'{sucees_fix_folder}/{args.file}')
                    print("DrRepair compiled!")                             #DrRepair 修復後無錯誤訊息
                    break
            elif(coderepair_len == 0 and DrRepair_len == 0):
                 #coderepair，DrRepair 修復後皆無錯誤訊息
                shutil.copyfile(os.path.join(copy_path ,copy_file),f'{two_sucees_folder}/co_{args.file}') #修復結果複製到two_sucees_folder資料夾
                shutil.copyfile('data/DrRepair.c',f'{two_sucees_folder}/Dr_{args.file}')
                print("two compiled!")
                break
            else:
                #coderepair，DrRepair 修復後錯誤訊息長度相同，則繼續迭代
                print("two compiled len same")
            
        
        
        
        
    elif args.idir:
            
        for file in get_dir_files(args.idir):
            
            copy_file = 'copy.c'
            copy_path = 'data'
            shutil.copyfile(f'{args.idir}/{file}',os.path.join(copy_path ,copy_file)) #將原檔案複製一份到copy.c
            print("filename:"+file)
            for i in range(5):
                
                if(i == 0 ):
                    DrRepair_fix(f'{args.idir}/{file}')   #跑DrRepair 模型,跑完結果在 data資料夾 裡的 DrRepair.c 檔 
                else:
                    DrRepair_fix('data/DrRepair.c')
                for j in range(5):
                    with open(os.path.join(copy_path ,copy_file), "r") as f:
                        old_code = f.read()
                    code_fix(os.path.join(copy_path ,copy_file) ,copy_file)  #跑coderepair 模型,跑完結果在 data資料夾 裡的 copy.c 檔 
                    with open(os.path.join(copy_path ,copy_file), "r") as f:
                        new_code = f.read()
                    if old_code.split() == new_code.split():
                        print("coderepair break!")
                        break
 
                DrRepair_len = len(compile_file('data/DrRepair.c'))       
                coderepair_len = len(compile_file(os.path.join(copy_path ,copy_file)))
                if (i>=4):#若修復五次
                    shutil.copyfile(os.path.join(copy_path ,copy_file) ,f'{fail_fix_folder}/co_{file}')
                    shutil.copyfile('data/DrRepair.c',f'{fail_fix_folder}/Dr_{file}')
                    print("try over 5 times! fix error! move it to error data!") 
                    break
                elif (DrRepair_len > coderepair_len):     #coderepair 修復後錯誤訊息較少
                    if coderepair_len:           
                        with open(os.path.join(copy_path ,copy_file), "r") as f:
                            coderepair = f.read()
                        with open('data/DrRepair.c', 'w') as f:
                            f.write(coderepair)                        #將DrRepair.c 檔內容 用copy.c 檔內容取代
                    else:
                        shutil.copyfile(os.path.join(copy_path ,copy_file),f'{sucees_fix_folder}/{file}')
                        print("coderepair compiled!")                             #coderepair 修復後無錯誤訊息
                        break
                elif(coderepair_len > DrRepair_len):    #DrRepair 修復後錯誤訊息較少
                    if DrRepair_len:
                        with open('data/DrRepair.c', "r") as f:
                            DrRepair = f.read()
                        with open(os.path.join(copy_path ,copy_file), "w") as f:
                            f.write(DrRepair)                           #將copy.c 檔內容 用DrRepair.c 檔內容取代
                    else:
                        shutil.copyfile('data/DrRepair.c',f'{sucees_fix_folder}/{file}')
                        print("DrRepair compiled!")                             #DrRepair 修復後無錯誤訊息
                        break
                elif(coderepair_len == 0 and DrRepair_len == 0):
                    #coderepair，DrRepair 修復後皆無錯誤訊息
                    shutil.copyfile(os.path.join(copy_path ,copy_file),f'{two_sucees_folder}/co_{file}') #修復結果複製到two_sucees_folder資料夾
                    shutil.copyfile('data/DrRepair.c',f'{two_sucees_folder}/Dr_{file}')
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
            
def code_fix(file_path,filename):
    if (len(compile_file(file_path))):      #查看compiler 訊息長度       
        auto_fix_str(file_path,file_path,filename)    #修復字串錯誤    
        if (len(compile_file(file_path))):      #查看compiler 訊息長度   
            error_num = len(compile_file(file_path))    #儲存compiler 訊息長度  
            auto_model_fix(file_path,file_path,filename,model)    #修復語法錯誤   
            if (len(compile_file(file_path))== error_num):
                #若語法修復完compiler訊息長度不變                                                         
                return 2
            elif (len(compile_file(file_path))):
                #若語法修復完還是有錯 
                return 0
            else:
                #修復完compiler無錯誤訊息
                print("code fix success!")
                return 1
        else:
            #修復完compiler無錯誤訊息
            print("code fix success!")
            return 1

    else:
        #修復完compiler無錯誤訊息
        print("code fix success!")
        return 1
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
    
    with open('data/DrRepair.c', 'w') as f:
        f.write(ans)
    

if __name__ == '__main__':
    
    two_sucees_folder = 'data/two_mix_sucess'
    sucees_fix_folder = 'data/mix_sucess'
    fail_fix_folder = 'data/mix_fail'
    
    create_folder(two_sucees_folder)
    create_folder(sucees_fix_folder)
    create_folder(fail_fix_folder)


    parser = argparse.ArgumentParser(description='fix printf error code files by using model')

    parser.add_argument('-i', '--idir', type=str, help='path to the input directory')
    parser.add_argument('-f', '--file', type=str, help='file to be processed')

    opts = parser.parse_args()
    
    run_code_fix(opts)
    
    
