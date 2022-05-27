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
tokenize = C_Tokenizer().tokenize



filename = "model/c1.c"
folder_path = f'{filename}'

file_data = ""
line_column = 1

df = pd.read_csv('data/printf_para.csv')
code = df['correct'][81000]
print(code)
tokenized_code, name_dict, name_seq = tokenize(code)
print(tokenized_code, name_dict, name_seq)
#print(tokenized_code.split())
codelength = len(tokenized_code.split())
#print(codelength)


