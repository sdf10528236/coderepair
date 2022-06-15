import pandas as pd


if __name__ == '__main__':
    files = ['../data/printf_new1.csv','../data/printf_new2.csv','../data/printf_new4.csv']
    
    df = pd.concat(
    (pd.read_csv(file, usecols=['correct','wrong'], dtype={ 'name': str, 'tweet':str}) for file in files), ignore_index=True)
    
    df = df.sample(frac=1).reset_index(drop = True)
    print(df)
    df.to_csv("../data/printf_new.csv",
             encoding='utf-8', index=False)