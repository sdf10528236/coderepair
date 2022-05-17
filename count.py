import os
correct_count = 0
fail_count = 0
all_count = 0
dir = "data/pdata_copy"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        all_count += 1


dir = "data/fsdata_2"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        correct_count += 1


dir = "data/ffdata_2"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        fail_count += 1
print("總資料量：",correct_count+fail_count)
print("成功修:",correct_count)
print("失敗修：",fail_count)

print("修復率：",correct_count/(correct_count+fail_count))