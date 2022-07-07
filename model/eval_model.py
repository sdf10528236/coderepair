import os, subprocess
import re
from model.model_fix import auto_model_fix
from difflib import SequenceMatcher
import tensorflow as tf
from model.model_train import create_model
from model.model_fix import predict_date_strs
import time

sucees_fix_folder = 'data/sucess'
fail_fix_folder = 'data/fail'
MAX_TIMES = 5

class EvalModel:
    def __init__(self, modelpath):
        start = time.time()
        print("Create Model")
        self.model = create_model()
        end = time.time()
        print("Spent time = ", end-start)
        start = end
        print("Load Model Weights")
        weights = tf.train.latest_checkpoint(modelpath)
        self.model.load_weights(weights).expect_partial()
        end = time.time()
        print("Spent time = ", end-start)

    def compile_file(self, file):
        p = subprocess.run(['gcc', file, '-o', '/dev/null'], capture_output=True)
        #print(p.stderr.decode("utf-8"))
        result = p.stderr.decode("utf-8") #.splitlines()
        return result

    # def compile_code(self):
    #     self.write_to_file("temp.c")
    #     result = self.compile_file("temp.c")
    #     result = result.replace("temp.c", "<stdin>")
    #     return result.splitlines()

    def compile_code(self):
        p = subprocess.run(['gcc', '-o', '/dev/null', '-xc', '-'], 
            input=str.encode(self.code), capture_output=True)
        result = p.stderr.decode().splitlines()
        return result

    def str_warning(self, compile_result):
        printf_fix_line = {}
        for text in compile_result:
            text = text.replace("‘","\'")
            text = text.replace("’","\'")
            p = [m.span()for m in re.finditer("\'", text)]
            #print(text)
            #print(p)
            if len(p) != 0:
                for i in range(len(p)):

                    if i % 2 == 0:
                        position_start = p[i][1]
                    else:
                        position_end = p[i][0]
                        string = text[position_start:position_end]
                        #print(string)
                        
                        if SequenceMatcher(None, "printf", string).ratio() > 0.7:
                            colon_positions = [m.span()
                                            for m in re.finditer(":", text)]  # 冒號位置
                            colume_start = [m.span()
                                            for m in re.finditer(f"<stdin>:", text)]  # （檔名：）位置
                            if  len(colume_start)>0 :
                                column_end = min((i[0] for i in colon_positions if i[0] >
                                            colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))

                                column_line = text[colume_start[0][1]:column_end]

                                if column_line not in printf_fix_line:
                                    printf_fix_line[column_line] = string
                                    #print(printf_fix_line)
        

        return printf_fix_line

    def fix_str(self, printf_fix_line):
        line_column = 1
        newcode = []
        if (len(printf_fix_line) == 0  ):
            print("no str error!")
            return 0
        for line in self.code.split("\n"):
            if str(line_column) in printf_fix_line:
                line = line.replace(
                    printf_fix_line[str(line_column)], "printf")
            newcode.append(line)
            line_column = line_column+1
        self.code = "\n".join(newcode)

    def auto_fix_str(self, compile_result):
        printf_fix_line = self.str_warning(compile_result)
        self.fix_str(printf_fix_line)

    def find_column(self, compile_result):
        column = []
        #print(compile_result)
        for text in compile_result:
            p = [m.span()for m in re.finditer('error', text)]
            w = [m.span()for m in re.finditer('warning', text)]
            if(len(p) > 0 or len(w)>0):
                # print(text)
                colon_positions = [m.span()
                                for m in re.finditer(":", text)]  # 冒號位置
                colume_start = [m.span()
                                for m in re.finditer("<stdin>:", text)]
                #print(colume_start)
                if (len(colume_start)>0) :
                    column_end = min((i[0] for i in colon_positions if i[0] >
                                colume_start[0][1]), key=lambda x: abs(x - colume_start[0][1]))
                    n = text[colume_start[0][1]:column_end]
            
                    if n not in column:
                        column.append(text[colume_start[0][1]:column_end]) 
                else: 
                    continue
        #print(column)
        return column

    def column_fix(self, column):
        global total
        line_column = 1
        newcode = []
        for line in self.code.split("\n"):
            if str(line_column) in column:
                printf_positions = [m.span()
                                    for m in re.finditer('printf', line)]
                if(len(printf_positions) > 0):
                    
                    wrong_str = line[printf_positions[0][0]:]

                    break_positions = [m.span()
                                    for m in re.finditer('break', wrong_str )]
                    right_positions = [m.span()
                                    for m in re.finditer('}', wrong_str )]
                    
                    if len( break_positions ):
                        wrong_str = wrong_str[:break_positions[0][0]]
                    elif len( right_positions ):
                        wrong_str = wrong_str[:right_positions[0][0]]
                    print("model input: "+wrong_str)
                    try:
                        fix_line = predict_date_strs(wrong_str.strip(), self.model)
                        print("model output: "+fix_line)
                        
                        if len( break_positions ):
                            fix_line =  fix_line + " break;"
                        elif len( right_positions ):
                            fix_line =  fix_line + " }"

                        line = line[:printf_positions[0][0]] + fix_line
                    except:
                        line = line
                        #print(INPUT_CHARS)
            newcode.append(line)
            line_column = line_column+1
            # print(file_data)

        self.code = "\n".join(newcode)

    def auto_model_fix(self, compile_result):
        #compile_result = run_compiler(folder_path)
        column = self.find_column(compile_result)
        self.column_fix(column)

    def code_fix(self):
        compile_result = self.compile_code()
        if (len(compile_result)):
            self.auto_fix_str(compile_result)
            compile_result = self.compile_code()
            if (len(compile_result)):
                error_num = len(compile_result)
                # Modify the following
                self.auto_model_fix(compile_result)
                new_compile_result = self.compile_code()
                if (len(new_compile_result)== error_num):
                    return 2
                elif (len(new_compile_result)):
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

    def write_to_file(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.code)        

    def try_fix_file(self, dir, file):
        print("\nFile:", file)
        fp = open(os.path.join(dir, file), "r")
        self.code = fp.read()
        fp.close()        
        for i in range(MAX_TIMES):
            if(self.code_fix()==1):
                self.write_to_file(f'{sucees_fix_folder}/{file}')
                print("move to success folder")
                return 1
            if(self.code_fix()==2):
                self.write_to_file(f'{fail_fix_folder}/{file}')
                print("model fixco error ! fix error! move it to error data!") 
                return 0
        self.write_to_file(f'{fail_fix_folder}/{file}')
        print("try over 5 times! fix error! move it to error data!")  
        return 0
    #程式修復流程
    def coderepair_fix_file(self, filepath ):
        print("\nFile:", filepath )
        fp = open(filepath, "r")
        self.code = fp.read()
        fp.close()        
        for i in range(MAX_TIMES):
            if(self.code_fix()==1):
                self.write_to_file(filepath)
                return 1
            if(self.code_fix()==2):
                self.write_to_file(filepath)
                return 0
        self.write_to_file(filepath)  
        return 0
    #程式修復流程


#print(compile_string(s))