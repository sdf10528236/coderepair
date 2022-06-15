# Code Repair

#### DATA：
[LINK](https://drive.google.com/drive/folders/1NfAx5mKUyAcAq9oc7q_1CW1UYczY8UuK?usp=sharing)<br>

1. **p3data資料夾** 裡面是從codinghere程式平台篩選出來有printf輸出函式錯誤的資料(有排除特殊錯誤)  
2. **printf_new.csv** 模型訊練的資料(由create_data 資料夾裡的create_printf_train_data.py 產出)  
3. **training_token_printfnew資料夾** 模型訓練完後的參數
4. **all_dicts.npy** 程式碼標記化的字典

## 第一次用看這裡(修復程式碼)
1. **先從DATA中下載上述1.2.3.4.檔案，在coderepair中創建一個名為 data 的資料夾**。
2. **將p3data資料夾、printf_new.csv 放入data資料夾。**  
**將training_token_printfnew資料夾、all_dicts.npy 放入model資料夾。**<br>
3. **下指令： python main.py -i ( 資料夾路徑 ) ，會開始跑修復流程。 ex.python main.py -i data/p3data**<br> 
(修復成功的檔案會複製到data/sucees資料夾;修復失敗會複製到data/fail資料夾)<br> 
4. **main.py跑完後，輸入python count.py ，查看修復率**<br>  


## 若要更改模型
**1. 進到model資料夾裡的model_train.py，修改checkpoint_path參數(訓練參數除存的資料夾)，更改模型並進行訓練**<br>
**2. 訓練好後，若是只想測試一下自己的模型訓練成果可以到model_test.py**裡，修改checkpoint_path參數(訓練參數除存的資料夾)，並啟用程式碼，會印出model input: 和 model output:。<br>(主要會使用model資料夾裡的c1.c檔做測試)<br>
**3. 訓練好後，到model_fix.py的column_fix函式裡更改checkpoint_path參數(同model_train.py)，修改完後即可使用main.py**<br>


# 資料夾、py檔 詳細說明

## 主程式

### main.py
-主要修復流程的程式碼(-i 資料夾 )<br>
建議一次跑500筆內(500筆約要跑快兩小時)<br>
下指令： ex. python main.py -i data/p2data
### count.py 
-main.py跑完後,計算修復率的程式碼<br>
*要用時,請先更改裡面的dir參數(資料夾路徑)




## 資料夾 (主要會用到data,model資料夾)

### compiler 資料夾
##### compile_msg.py 
- 會印出程式碼編譯(gcc)的錯誤訊息 (-i 資料夾 / -f 檔案)

##### movedata.py 
- 可以移動資料到別的資料夾的程式碼

### create_data 資料夾
##### auto_corrupt_syntax.py
 - 用來破壞正確程式碼的程式(來源：Drrepair) <br>
 主要用到的函式：auto_corrupt_synta

##### concact_csv.py 
- 用來合併兩個以上csv檔的程式碼

##### create_printf_train_data.py 
- 用來產生輸出函數的測試、訓練資料(csv)，主要有三種資料：<br>
1. printf("%d",a);<br>
2. printf("hello");<br>
3. printf("sdfsdgqw");

 ##### find_codinghere_printf_error_data.py
 - 用來找出codinghere data裡有輸出函式錯誤的程式碼


 ##### get_codinghere_printf_correct_data.py
 - 用來找出codinghere data裡輸出函式語法正確的輸出函式資料
 ex.printf("%d", s[i]);

### data 資料夾
-原本沒有此資料夾，請自己創建一個(檔名：data)。


### model 資料夾 


##### model_train.py
-用來訓練模型的程式碼

##### model_test.py
-用來測試訓練好的模型的程式碼

##### model_fix.py
-用來修復有輸出函數語法錯誤的程式碼
主要是main.py會引用

### str_fix 資料夾
##### fix_printf_scanf.py
-用來修復有輸出函數'字串'錯誤的程式碼

