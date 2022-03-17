import pandas as pd


if __name__ == '__main__':
    files = ['../data/printf01.csv','../data/printf02.csv']
    df = pd.concat(
    (pd.read_csv(file, usecols=['correct','wrong'], dtype={ 'name': str, 'tweet':str}) for file in files), ignore_index=True)
    print(df)