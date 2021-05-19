#!/usr/bin/env python3
import os
import sys

def main(argv):
    path = argv[0]
    flist = scanner(path)
    for name in flist:
        os.system("mpirun -np 4 ~/builds/q-e/bin/pw.x < " + name)

# get all files in path
def scanner(path):
    flist = []

    for root, dirs, files in os.walk(path):
        for file in files:
            flist.append(os.path.join(root,file))

    return flist

if __name__ == "__main__":
    main(sys.argv[1:])
