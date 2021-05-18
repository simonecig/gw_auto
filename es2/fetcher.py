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
                      names=['name', 'description', 'type'])

    # read only the row containing compound name
    name = pd.read_csv(fname, sep=';', skipinitialspace=True, skiprows=1,
                       index_col=False, header=None,
                       names=['name', 'x', 'y', 'z'], nrows=1)

    # generate q-e input file
    qe.creator(pos, str(name['name'][0]))

    print("done!")


if __name__ == "__main__":
    main(sys.argv[1:])
