#!/usr/bin/env python3

import pandas as pd
import os
import numpy as np
import sys
import all_runner
import single_converter
import extra

def file_generator(pos_path):

    start = 30
    end = 100
    step = 5

    pos_flist = extra.scanner(pos_path)

    # loop over all files
    for i in range(len(pos_flist)):

        name = pos_flist[i]
        print(i, "/", len(pos_flist))

        # loop over all cutoff values
        for cutoff in range(start, end, step):

            # generate input file
            single_converter.convert([name, cutoff])


# generate and compute
def main(argv):

    file_generator(argv[0])
    # all_runner.run(argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
