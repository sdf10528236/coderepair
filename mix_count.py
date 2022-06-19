import os


correct_count = 0
fail_count = 0




dir = 'data/two_mix_sucess'  #修復成功程式碼的資料夾
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        correct_count += 1
correct_count = correct_count/2

dir = 'data/mix_sucess'  #修復成功程式碼的資料夾
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        correct_count += 1

dir = 'data/mix_fail'   #修復失敗程式碼的資料夾
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        fail_count += 1
fail_count = fail_count/2

print("總修復資料量：",correct_count+fail_count)
print("成功修復:",correct_count)
print("失敗修復：",fail_count)
print("修復率：",correct_count/(correct_count+fail_count))