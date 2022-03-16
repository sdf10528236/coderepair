import os

if __name__ == '__main__':

    folder_path = '/home/laz/Program/coderepair/data/codinghere_data/'
    folderList = os.listdir(folder_path)
    folderList.sort()
    #print(folderList)
    cnt = 0
    data = {
        "correct": [],
        "wrong": [],
    }
    df = pd.DataFrame(data)
    cur_line_strs = []

    for base in folderList:
        path = folder_path + base + "/" + "correct"
        fileList = os.listdir(path)
        fileList.sort()
        for file in fileList:
            filepath = path + "/" + file
            #print(filepath)
            f = open(filepath)
            try:
                cur_line_strs.append(f.read())
                print(len(cur_line_strs))
            except:
                continue
