import os
correct_count = 0
fail_count = 0
all_count = 0
dir = "data/pdata_copy"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        all_count += 1
print(all_count)

dir = "data/fsdata"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        correct_count += 1
print(correct_count)

dir = "data/ffdata"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        fail_count += 1

print(fail_count)

print(correct_count/(correct_count+fail_count))