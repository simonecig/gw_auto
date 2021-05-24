import pandas as pd
import os
import numpy as np
import sys
import gw100_to_qe as qe


# Convert a single GW100 file in
# a qe input file, which is saved
# in the "./output" folder.
# Requires file name as argument
def convert(argv):

    # get file name
    fname = argv[0]

    pos, name = qe.fetch(fname)

    # generate q-e input file
    if len(argv) > 1:
        qe.creator_wCutoff(pos, name, int(argv[1]))
    else:
        qe.creator(pos, name)


if __name__ == "__main__":
    convert(sys.argv[1:])
