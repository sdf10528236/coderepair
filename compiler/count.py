import os
correct_count = 0
fail_count = 0
all_count = 0
dir = "../data/pdata_copy"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        all_count += 1
print(all_count)