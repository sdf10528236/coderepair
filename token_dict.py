"""
Copyright 2017 Rahul Gupta, Soham Pal, Aditya Kanade, Shirish Shevade.
Indian Institute of Science.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import pandas as pd
from util.c_tokenizer import C_Tokenizer
import os
import numpy as np
tokenize = C_Tokenizer().tokenize

def build_dictionary(token_strings, drop_ids, tl_dict={}):

    def build_dict(list_generator, dict_ref):
        
        for tokenized_code in list_generator:
            #print(tokenized_code)
            for token in tokenized_code.split():
                if drop_ids and '_<id>_' in token:
                    continue
                token = token.strip()
                if token not in dict_ref:
                    dict_ref[token] = len(dict_ref)

    tl_dict['_pad_'] = 0
    tl_dict['_eos_'] = 1
    #tl_dict['~'] = 2

    if drop_ids:
        #tl_dict['_<id>_@'] = 3
        tl_dict['_<id>_@'] = 2

    if type(token_strings) == list:
        token_strings_list = token_strings

        for token_strings in token_strings_list:
            for key in token_strings:
                for problem_id in token_strings[key]:
                    build_dict((prog for prog
                                 in token_strings[key][problem_id]), tl_dict)
    else:
        for key in token_strings:
            for problem_id in token_strings[key]:
                
                build_dict((prog  for prog
                        in token_strings[key][problem_id]), tl_dict)

    print ('dictionary size:', len(tl_dict))
    assert len(tl_dict) > 4
    return tl_dict
if __name__ == '__main__':
    now_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = now_path+'/data/p2data/'
    folderList = os.listdir(folder_path)
    folderList.sort()
    token_strings = {'correct': {}, 'wrong': {}}
    
    cnt = 0

    for base in folderList:
        path = folder_path + base
        #print(path)
        
        
        file_code = ""
        line_column = 1
        with open(path, "r") as f:

            for line in f:
               
                    

                file_code += line

                line_column = line_column+1
            #print(file_code)
            tokenized_code, name_dict, name_seq = tokenize(file_code)
            token_strings['correct'][cnt] = [(tokenized_code)]
    
            cnt+=1
    df = pd.read_csv("data/printf_all.csv")
    
    for strs in df["correct"]:
        #print(strs)
        tokenized_code, name_dict, name_seq = tokenize(strs)
        token_strings['correct'][cnt] = [(tokenized_code)]
        cnt+=1
    for strs in df["wrong"]:
        #print(strs)
        tokenized_code, name_dict, name_seq = tokenize(strs)
        token_strings['correct'][cnt] = [(tokenized_code)]
        cnt+=1
    
    all_dicts = build_dictionary(token_strings,True)
    print(all_dicts)
    np.save(os.path.join(now_path+'/model/', 'all_dicts.npy'), all_dicts)

  