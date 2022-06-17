import os
import shutil


if __name__ == '__main__':

    folder_path = '/home/sdf/Program/coderepair/data/codinghere_data/'
    folderList = os.listdir(folder_path)
    folderList.sort()
    #print(folderList)
    sum = 0
    

    for base in folderList:
        path = folder_path + base + "/" + "erroneous"
        fileList = os.listdir(path)
        fileList.sort()
        
        for file in fileList:
            filepath = path + "/" + file
            
            
            shutil.copyfile(f'{filepath }',f'../data/codinghere_err_data/{file}')  #複製並移動檔案
    

    # all_list = os.listdir('/home/laz/Program/coderepair/compiler/pdata')
    # print(len(all_list))