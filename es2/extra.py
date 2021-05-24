#!/usr/bin/env python3
import os

# get all files in path
def scanner(path):
    flist = []

    for root, dirs, files in os.walk(path):
        for file in files:
            flist.append(os.path.join(root,file))

    return flist
