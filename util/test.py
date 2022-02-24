import regex as re
import pandas as pd
import collections
from c_tokenizer import C_Tokenizer
Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])


def tokenize_code(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('comment',
         r'\/\*(?:[^*]|\*(?!\/))*\*\/|\/\*([^*]|\*(?!\/))*\*?|\/\/[^\n]*'),
        ('directive', r'#\w+'),
        ('string', r'"(?:[^"\n]|\\")*"?'),
        ('char', r"'(?:\\?[^'\n]|\\')'"),
        ('char_continue', r"'[^']*"),
        ('number',  r'[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'),
        ('include',  r'(?<=\#include) *<([_A-Za-z]\w*(?:\.h))?>'),
        ('op',
         r'\(|\)|\[|\]|{|}|->|<<|>>|\*\*|\|\||&&|--|\+\+|[-+*|&%\/=]=|[-<>~!%^&*\/+=?|.,:;#]'),
        ('name',  r'[_A-Za-z]\w*'),
        ('whitespace',  r'\s+'),
        ('nl', r'\\\n?'),
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' %
                         pair for pair in token_specification)

    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            yield "stop"
        else:
            if kind == 'ID' and value in keywords:
                kind = value
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


if __name__ == '__main__':

    df = pd.read_csv('../data/test.csv')

    code = df['wrong'][1]
    tokenize = C_Tokenizer().tokenize
    tokenized_code, name_dict, name_seq = tokenize(code)

    print(tokenized_code)
    print(name_dict)
    print(name_seq)
