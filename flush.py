import os

folder1 = "" # Path to first image folder
folder2 = "" # Path to second image folder
logfile = "log.txt"

originals = set(os.listdir(folder2))
metallics = set(os.listdir(folder1))

with open(logfile, "r") as output:
    lines = output.readlines()
    for line in lines:
        filename = line.strip()
        print(os.path.join(folder1, filename))
        if os.path.exists(os.path.join(folder1, filename)):
            os.remove(os.path.join(folder1, filename))
        if os.path.exists(os.path.join(folder2, filename)):
            os.remove(os.path.join(folder2, filename))
