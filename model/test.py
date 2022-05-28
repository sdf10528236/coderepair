import numpy as np
import pandas as pd
import string
from util.c_tokenizer import C_Tokenizer
# INPUT_CHARS = "".join(
#     sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=~@#$^|\n\t`{}\\() ,;.\"[]%'!&?"

# OUTPUT_CHARS = "".join(
#     sorted(set("".join(string.ascii_letters)))) + " _*/0123456789+-=~@#$^|\n\t`{}\\() ,;.\"[]%'!&?"

tokenize = C_Tokenizer().tokenize
INPUT_CHARS = np.load('all_dicts.npy',allow_pickle=True).item()
OUTPUT_CHARS = np.load('all_dicts.npy',allow_pickle=True).item()
id_to_token_dict = {v:k for k,v in INPUT_CHARS.items()}

def data_str_to_token(data_str):
    #print(data_str)
    tokenized_code, name_dict, name_seq = tokenize(data_str)
    print(tokenized_code, name_dict, name_seq)
    tokenized_code_list = tokenized_code.split()
    
        
    tokenized_code_list=[]
    #print(tokenized_code.split())
    for token in tokenized_code.split():
        
        if '_<id>_' in token:
            
            token = '_<id>_@'
            
        tokenized_code_list.append(token)
    return tokenized_code_list 
   
def data_str_to_ids(date_str, chars):
    tokenized_code_list = data_str_to_token(date_str)
    #print(tokenized_code_list)
    return [chars[f'{token}'] for token in tokenized_code_list]

def prepare_date_strs(data_strs, chars=INPUT_CHARS):
    
    X_ids = [data_str_to_ids(dt, chars) for dt in data_strs]
    #print( X_ids)
    xlen = max(len(x) for x in X_ids)
    y = []
    for i in range(len(X_ids)):
        y.append(X_ids[i] + [0]*(xlen-len(X_ids[i])))
    #print(np.array(y))
    return np.array(y)
def create_dataset(x, y):
    return prepare_date_strs(x, INPUT_CHARS), prepare_date_strs(y, OUTPUT_CHARS)

def ids_to_token(ids, chars=id_to_token_dict):
    
        
    return [" ".join(chars[index] for index in ids)]

def token_to_str(token):
    print(token)

def tokens_to_source(tokens, name_dict, clang_format=False, name_seq=None):
    result = ''
    type_ = None

    reverse_name_dict = {}
    name_count = 0

    for k, v in name_dict.items():
        reverse_name_dict[v] = k

    for token in tokens.split():
        try:
            prev_type_was_op = (type_ == 'op')

            type_, content = token.split('>_')
            type_ = type_.lstrip('_<')

            if type_ == 'id':
                if name_seq is not None:
                    content = name_seq[name_count]
                    name_count += 1
                else:
                    try:
                        content = reverse_name_dict[content.rstrip('@')]
                    except KeyError:
                        content = 'new_id_' + content.rstrip('@')
            elif type_ == 'number':
                content = content.rstrip('#')

            if type_ == 'directive' or type_ == 'include' or type_ == 'op' or type_ == 'type' or type_ == 'keyword' or type_ == 'APIcall'or type_ == 'pa':
                if type_ == 'op' and prev_type_was_op:
                    result = result[:-1] + content + ' '
                else:
                    result += content + ' '
            elif type_ == 'id':
                result += content + ' '
            elif type_ == 'number':
                result += '0 '
            elif type_ == 'string':
                result += '"String" '
            elif type_ == 'char':
                result += "'c' "
        except ValueError:
            if token == '~':
                result += '\n'

    if not clang_format:
        return result

  

if __name__ == '__main__':
    df = pd.read_csv('data/printf_autocreate.csv')
    
    
    X_train, Y_train = create_dataset( df['correct'][15:20],df['wrong'][15:20])
    #print(X_train)
    #print(ids_to_token(X_train[3]))
    token = ids_to_token(X_train[4])[0]
    print(token)
    print(token.split())
    print(tokens_to_source(token,INPUT_CHARS, False,['b', 'QVd', 'tX']))
    #print(ids_to_token(X_train))
   
