import os, random, shutil
def moveFile(fileDir):
        pathDir = os.listdir(fileDir)    #取圖片的原始路徑
        filenumber=len(pathDir)
        picknumber=1000 #從資料夾中取一定數量
        sample = random.sample(pathDir, picknumber)  #隨機選取picknumber數量的樣本圖片
        print (sample)
        cnt = 1
        for name in sample:
            shutil.move(f"{fileDir}/{name}", f"{tarDir}/{cnt}.c")
            cnt = cnt+1
        return

if __name__ == '__main__':
    fileDir = "../data/codinghere_err_data"    #源圖片資料夾路徑
    tarDir = '../data/wrong_1000'    #移動到新的資料夾路徑
    moveFile(fileDir)   