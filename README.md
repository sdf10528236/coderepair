# Code Repair

## compiler 資料夾
##### compile_msg.py 
- 會印出程式碼編譯(gcc)的錯誤訊息 (-i 資料夾 / -f 檔案)

##### movedata.py 
- 可以移動資料到別的資料夾的程式碼

## create_data 資料夾
##### auto_corrupt_syntax.py
 - 用來破壞正確程式碼的程式(來源：Drrepair) 主要用到的函式：auto_corrupt_synta

##### concact_csv.py 
- 用來合併兩個以上csv檔的程式碼

##### create_printf_train_data.py 
- 用來產生輸出函數的測試、訓練資料(csv)，主要有三種資料：
1.printf("%d",a);
2.printf("hello");
3.printf("sdfsdgqw");
 
 ##### find_codinghere_printf_error_data.py
 - 用來找出codinghere data裡有輸出函式錯誤的程式碼


 ##### get_codinghere_printf_correct_data.py
 - 用來找出codinghere data裡輸出函式語法正確的輸出函式資料
 ex.printf("%d", s[i]);

## data 資料夾
-原本沒有此資料夾請自己創建一個(檔名：data)，將下面 DATA的資料都放入此資料夾
### DATA
[LINK](https://drive.google.com/drive/folders/1NfAx5mKUyAcAq9oc7q_1CW1UYczY8UuK?usp=sharing)
1.pdata2 資料夾裡是從codinghere程式平台篩選出來有printf輸出函式錯誤的資料
2.printf_autocreate.csv 模型訊練的資料(由create_data 資料夾裡的create_printf_train_data.py 產出)

## model 資料夾 
##### model_train.py
-用來訓練模型的程式碼

##### model_test.py
-用來測試訓練好的模型的程式碼

##### model_fix.py
-用來修復有輸出函數語法錯誤的程式碼
主要是main.py會引用

## str_fix 資料夾
##### fix_printf_scanf.py
-用來修復有輸出函數'字串'錯誤的程式碼


## main.py
-主要修復流程的程式碼(-i 資料夾 ex.python main.py -i data/p2data)
建議一次跑500筆內(500筆約要跑快兩小時)
## count.py 
-main.py跑完後,計算修復率的程式碼
*要用時,請先更改裡面的dir參數(資料夾路徑)