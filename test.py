import os 

with open("c1.c", "r") as f:
    old_code = f.read()

    print( old_code.split() )

with open("c2.c", "r") as f:
    new_code = f.read()
    print( new_code.split() )
print(old_code == new_code)
print(old_code.split() == new_code.split())