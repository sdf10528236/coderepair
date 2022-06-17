from str_fix.fix_printf_scanf import auto_fix_str
from model.model_fix import auto_model_fix
from model.model_train import create_model
import argparse
import os
import subprocess
import shutil
import os
import tensorflow as tf
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


def get_dir_files(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-1:]=='c']
    files.sort()
    return files

def run_code_fix(args): #filepath, compiler_path="gcc"):
    
    if args.file:
        shutil.copyfile(f'{args.file}',f'copy.c')
        file = 'copy.c'
        print(args.file)
        code_fix(file ,file)
        
        
    elif args.idir:
        input_path = 'data/input_data'          
        if not os.path.isdir(input_path):  #創建一個input_data資料夾
            os.mkdir(input_path)
        else:
            shutil.rmtree(input_path)   #刪除並創建一個input_data資料夾
            os.mkdir(input_path)
                                             

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
                    #語法錯誤修復完compiler訊息長度不變 
                    shutil.copyfile(f'{input_path}/{file}',f'{fail_fix_folder}/{file}')
                    print("model fixco error ! fix error! move it to error data!") 
                    break
                elif (i >= 4):  #若修復五次
                    shutil.copyfile(f'{input_path}/{file}',f'{fail_fix_folder}/{file}')
                    print("try over 5 times! fix error! move it to error data!")  
        #程式修復流程


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
    
    
