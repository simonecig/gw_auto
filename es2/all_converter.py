import pandas as pd
import os
import numpy as np
import sys
import gw100_to_qe as qe
import json_parser as js

# Convert all GW100 files in a folder
# into input files that can be used for qe.
# The final data is saved in the "./output"
# folder.
# Requires folder name as argument
def main(argv):

    # get path
    flist = scanner(argv[0])

    # loop over files
    for fname in flist:

        # get positions and compund name
        pos, name = qe.fetch(fname)

        # generate q-e input file
        qe.creator(pos, name)

    print(len(flist), " file generated!")


# get all files in path
def scanner(path):
    flist = []

    for root, dirs, files in os.walk(path):
        for file in files:
            flist.append(os.path.join(root,file))

    return flist


if __name__ == "__main__":
    main(sys.argv[1:])
