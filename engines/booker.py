import os

for i in os.listdir():
    if ".bin" in i:
        print(r"- engines/"+i)
