from inspect import ismethoddescriptor
import os
import shutil


if __name__ == '__main__':

    folder_path = '/home/laz/Program/coderepair/data/codinghere_data/'
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
            
            
            shutil.copyfile(f'{filepath }',f'npdata/{file}')  #複製並移動檔案
    

    # all_list = os.listdir('/home/laz/Program/coderepair/compiler/pdata')
    # print(len(all_list))