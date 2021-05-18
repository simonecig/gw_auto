import pandas as pd
import numpy as np
import sys
import gw100_to_qe as qe


# TODO: make this a module
# TODO: get compund name from file
def main(argv):
    # get file name
    fname = argv[0]
    # read requested file
    pos = pd.read_csv(fname, sep='\s+', skipinitialspace=True, skiprows=2,
                      index_col=False, header=None,
                      names=['name', 'x', 'y', 'z'])
    # generate q-e input file
    qe.creator(pos, "BeO")
    # save file 
    # f = open("output/"+fname, 'w')
    # f.write(data_qe)
    print("done!")


if __name__ == "__main__":
    main(sys.argv[1:])
