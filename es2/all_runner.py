#!/usr/bin/env python3
import os
import sys
import extra

def run(argv):
    path = argv[0]
    flist = extra.scanner(path)
    for name in flist:
        os.system("mpirun -np 4 pw.x < " + name + " > " + name + "_out" + " 2> " + name + "_err")

if __name__ == "__main__":
    run(sys.argv[1:])
