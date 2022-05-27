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

from unicodedata import name
import pandas as pd
from util.c_tokenizer import C_Tokenizer
tokenize = C_Tokenizer().tokenize

def build_dictionary(token_strings, drop_ids, tl_dict={}):

    def build_dict(list_generator, dict_ref):
        for tokenized_code in list_generator:
            for token in tokenized_code.split():
                if drop_ids and '_<id>_' in token:
                    continue
                token = token.strip()
                if token not in dict_ref:
                    dict_ref[token] = len(dict_ref)

    tl_dict['_pad_'] = 0
    tl_dict['_eos_'] = 1
    tl_dict['~'] = 2

    if drop_ids:
        tl_dict['_<id>_@'] = 3

    if type(token_strings) == list:
        token_strings_list = token_strings

        for token_strings in token_strings_list:
            for key in token_strings:
                for problem_id in token_strings[key]:
                    build_dict((prog + ' ' + fix for prog,
                                fix in token_strings[key][problem_id]), tl_dict)
    else:
        for key in token_strings:
            for problem_id in token_strings[key]:
                
                build_dict((prog + ' ' + fix for prog,
                            fix in token_strings[key][problem_id]), tl_dict)

    print ('dictionary size:', len(tl_dict))
    assert len(tl_dict) > 4
    return tl_dict
if __name__ == '__main__':

    filename = "model/c1.c"
    folder_path = f'{filename}'

    file_data = ""
    line_column = 1

    df = pd.read_csv('data/printf_para.csv')
    code = df['correct'][81000]
    print(code)
    tokenized_code, name_dict, name_seq = tokenize(code)
    print(tokenized_code, name_dict, name_seq)
    print(tokenized_code.split())
    codelength = len(tokenized_code.split())
    print(codelength)
    token_strings = {'train': {}, 'validation': {}}
    #print(token_strings)
    token_strings['train'][0] = [(tokenized_code, "-1")]
    token_strings['train'][1] = [(tokenized_code, "-1")]
    token_strings['validation'][0] = [(tokenized_code, "-1")]
    token_strings['validation'][1] = [(tokenized_code, "-1")]
    print(token_strings)
    print(type(token_strings))
    
    print(build_dictionary(token_strings,True))




