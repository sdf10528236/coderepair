from str_fix.fix_printf_scanf import auto_fix_str
from model.model_fix import auto_model_fix
import argparse
import os
import subprocess
import shutil
import os
import tensorflow as tf 
from model.model_train import create_model
from difflib import SequenceMatcher
import re as regex
from model.model_fix import predict_date_strs

max_fix_times = 6

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

        checkpoint_path = "/home/jyw/Program/coderepair/model/training_autocreate/cp-{epoch:04d}.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        model = create_model()
        model.load_weights(latest).expect_partial()

        files = get_dir_files(args.idir)
        for file in files:
            shutil.copyfile(f'{args.idir}/{file}',f'{input_path}/{file}')
            print("\nfilename:"+file)
            filepath = os.path.join(input_path, file)
            # Try to fix at most max_fix_times times
            res = code_fix(filepath, file, model, max_fix_times)
            if res==1: # success
                shutil.copyfile(f'{input_path}/{file}',f'{sucees_fix_folder}/{file}')
                print("move to success folder")
            elif res==2: # fail
                shutil.copyfile(f'{input_path}/{file}',f'{fail_fix_folder}/{file}')
                print("model fix error ! fix error! move it to error data!") 
            elif res==3:  # 修復次數滿了
                shutil.copyfile(f'{input_path}/{file}',f'{fail_fix_folder}/{file}')
                print(f"try over {max_fix_times} times! fix error! move it to error data!")  
        #程式修復流程


def compile_file(file):
    p = subprocess.run(['gcc', file], capture_output=True)
    #print(p.stderr.decode("utf-8"))
    result = p.stderr.decode("utf-8").splitlines()
    return result

def fix_str(old_file, new_file, printf_fix_line):
    line_column = 1
    file_data = ""
    if len(printf_fix_line) == 0:
        print("no str error!")
        return
    with open(old_file, "r") as f:
        for line in f:
            if str(line_column) in printf_fix_line:
                line = line.replace(printf_fix_line[str(line_column)], "printf")
            file_data += line
            line_column = line_column+1
    with open(new_file, "w") as f:
        f.write(file_data)

def str_warning(filename, compile_msg):
    printf_fix_line = {}
    for text in compile_msg:
        text = text.replace("‘","\'")
        text = text.replace("’","\'")
        p = [m.span() for m in regex.finditer("\'", text)]
        #print(text)
        #print(p)
        for i in range(len(p)):
            if i % 2 == 0:
                position_start = p[i][1]
            else:
                position_end = p[i][0]
                string = text[position_start:position_end]
                #print(string)
                
                if SequenceMatcher(None, "printf", string).ratio() > 0.7:
                    colon_positions = [m.span() for m in regex.finditer(":", text)]  # 冒號位置
                    column_start = [m.span() for m in regex.finditer(f"{filename}:", text)]  # （檔名：）位置
                    if  len(column_start)>0 :
                        column_end = min((i[0] for i in colon_positions if i[0] >
                                        column_start[0][1]), key=lambda x: abs(x - column_start[0][1]))

                        column_line = text[column_start[0][1]:column_end]

                    if column_line not in printf_fix_line:
                        printf_fix_line[column_line] = string
                        #print(printf_fix_line)
    return printf_fix_line

def find_column(warning_text, filename):
    column = []
    #print(warning_text)
    for text in warning_text:
        p = [m.span()for m in regex.finditer('error', text)]
        if len(p) > 0:
            # print(text)
            colon_positions = [m.span() for m in regex.finditer(":", text)]  # 冒號位置
            colume_start = [m.span() for m in regex.finditer(f"{filename}:", text)]
            #print(colume_start)
            if len(colume_start)>0:
                column_end = min((i[0] for i in colon_positions if i[0] >
                              colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))
                n = text[colume_start[0][1]:column_end]
          
                if n not in column:
                    column.append(text[colume_start[0][1]:column_end]) 
            else: 
                continue
    return column

def column_fix2(old_file, new_file, column, model):
    line_column = 1
    file_data = ""
    with open(old_file, "r") as f:
        for line in f:
            if str(line_column) in column:
                printf_positions = [m.span() for m in regex.finditer('printf', line)]
                if len(printf_positions) > 0:
                    wrong_str = line[printf_positions[0][0]:]
                    print("model input: "+wrong_str, end='')
                    try:
                        fix_line = predict_date_strs([wrong_str],model)[0]
                        print("model output: "+fix_line)
                        line = line[:printf_positions[0][0]] + fix_line + "\n"
                    except:
                        line = line
                        #print(INPUT_CHARS)
            file_data += line
            line_column = line_column+1
        # print(file_data)
    with open(new_file, "w") as f:
        f.write(file_data)

def column_fix(old_file, new_file, column, model):
    file_lines = []
    tofix = []
    tofix_idxs = []
    with open(old_file, "r") as f:
        line_idx = 1
        for line in f:
            if line[-1] == "\n":
                line = line[:-1]
            line = line.replace("\t","  ")                
            prefix = line
            if str(line_idx) in column:
                printf_positions = [m.span() for m in regex.finditer('printf', line)]
                if len(printf_positions) > 0:
                    wrong_str = line[printf_positions[0][0]:]
                    tofix.append(wrong_str)
                    tofix_idxs.append(line_idx-1)
                    print(f"Line {line_idx}: " + wrong_str)
                    prefix = line[:printf_positions[0][0]]
            file_lines.append(prefix)
            line_idx = line_idx+1

    if len(tofix_idxs) > 0:
        try:
            # print("Model input: ", tofix)
            fix_lines = predict_date_strs(tofix, model)
            print("Model output: ", fix_lines)
            for i in range(len(tofix_idxs)):
                file_lines[tofix_idxs[i]] += fix_lines[i]
        except:
            print("Error Occurred!")
            quit()
        with open(new_file, "w") as f:
            f.write("\n".join(file_lines))

def code_fix(file_path, filename, model, max_fix_times):

    compile_msg = compile_file(file_path)
    for i in range(max_fix_times):
        if (len(compile_msg)):
            # Fix printf typo error
            printf_fix_line = str_warning(filename, compile_msg)
            if len(printf_fix_line) > 0:
                fix_str(file_path, file_path, printf_fix_line)
                compile_msg = compile_file(file_path)
            error_num = len(compile_msg)
            if (error_num):
                # auto_model_fix(file_path, file_path, filename, model)
                column = find_column(compile_msg, filename)
                column_fix(file_path, file_path, column, model)
                compile_msg = compile_file(file_path)
                error_num2 = len(compile_msg)
                if (error_num2 == error_num): # Or change to >= ?
                    return 2
                elif (error_num2 == 0):
                    print("code fix success!")
                    return 1
        else:
            print("code fix success!")
            return 1
    return 3

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
    
    
