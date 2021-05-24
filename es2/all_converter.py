import pandas as pd
import os
import numpy as np
import sys
import gw100_to_qe as qe
import extra

# Convert all GW100 files in a folder
# into input files that can be used for qe.
# The final data is saved in the "./output"
# folder.
# Requires folder name as argument
def convert(argv):

    # get path
    flist = extra.scanner(argv[0])


    # loop over files
    for fname in flist:

        # get positions and compund name
        pos, name = qe.fetch(fname)

        # generate q-e input file
        qe.creator(pos, name)

    print(len(flist), " file generated!")



if __name__ == "__main__":
    convert(sys.argv[1:])
