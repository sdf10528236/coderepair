import os
correct_count = 0
fail_count = 0
all_count = 0
dir = "data/pdata_copy"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        all_count += 1
print("總資料量：",all_count)

dir = "data/fsdata"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        correct_count += 1
print("成功修復:",correct_count)

dir = "data/ffdata"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        fail_count += 1

print("失敗修復：",fail_count)

print("修復率：",correct_count/(correct_count+fail_count))