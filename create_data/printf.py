import string
import random
number_of_strings = 5


for i in range(number_of_strings):
    print("printf(\""+"".join(random.choice(string.ascii_letters)
                              for _ in range(random.randint(1, 20)))+"\");")
