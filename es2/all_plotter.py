#!/usr/bin/env python3

import extra
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

# get output data from given path
# find en tot, homo, lumo, cutoff
# plot

def prepare(argv):

    input_path = argv[0]
    flist = special_scan(input_path)
    data = pd.DataFrame(columns=['name', 'cpu_time', 'wall_time', 'tot_en', 'cutoff'])

    for name in flist:

        print(name)

        # read file content
        f = open(name, 'r')
        content = f.readlines()
        #print(content)

        # get useful data
        cpu_time, wall_time, tot_en = output_parser(content)

        # get cutoff from name
        cutoff = get_cutoff(name)

        # get name
        parsed_name = get_name(name)

        # store data in pandas dataframe
        new_row = {'name': parsed_name, 'cpu_time': cpu_time, 'wall_time': wall_time,
                   'tot_en': tot_en, 'cutoff': cutoff}
        data = data.append(new_row, ignore_index=True)

    print(data)
    data.to_csv('plot_data.txt', sep='\t', index=False)


# find and return en toto, homo, lumo, cutoff
# from content
def output_parser(content):

    counter = 0 # discard first 2 word occurences
    cpu_time = 9999
    wall_time = 9999
    tot_en = 0
    cutoff = 0

    # get line with times
    line = content[-8].split()
    # check if it's the correct line
    if(line[0] == 'PWSCF'):

        minutes = 0
        seconds = 0
        line = line[2:]

        # if both m and s are present in cpu time
        if 'm' in line[0] and 's' in line[0]:
            splitted_line = line[0].split('m')
            minutes = float(splitted_line[0])
            seconds = float(splitted_line[1][:-1])
            line = line[2:]

        # if conly m are present in cpu time
        elif 'm' in line[0] and not 's' in line[0]:
            minutes = float(line[0][:-1])
            seconds = float(line[1][:-1])
            line = line[3:]

        # if only s are present in cpu time
        else:
            minutes = 0
            seconds =  float(line[0][:-1])
            line = line[2:]

        # compute time in seconds
        cpu_time = minutes * 60 + seconds

        # repeat all for wall time
        if 'm' in line[0] and 's' in line[0]:
            splitted_line = line[0].split('m')
            minutes = float(splitted_line[0])
            seconds = float(splitted_line[1][:-1])
            line = line[2:]

        elif 'm' in line[0] and not 's' in line[0]:
            minutes = float(line[0][:-1])
            seconds = float(line[1][:-1])
            line = line[3:]

        else:
            minutes = 0
            seconds =  float(line[0][:-1])

        wall_time = minutes * 60 + seconds


    # loop over lines and search for total energy
    # start from bottom and go up
    for i in range(len(content)):
        line = content[-i].split()
        if '!' in line:
            tot_en = line[4]
            break

    return cpu_time, wall_time, tot_en



# return only output files in given path
def special_scan(path):

    flist = extra.scanner(path)
    special_flist = []

    # loop over file names
    for fname in flist:
        # check if file is output but not error log
        if ('out' in fname) and not ('err' in fname):
            # store file name
            special_flist.append(fname)

    return special_flist


def plot(names):

    fig, ax = plt.subplots()
    data = pd.read_csv('plot_data.txt', sep='\t')
    #uniq = np.unique(data['name'])
    #np.savetxt("./samples/names.txt", uniq, fmt='%s')

    labels = []
    for i in names:
        current_data = data[data['name'] == i]
        twin = ax.twinx()
        labelpm, = twin.plot(current_data['cutoff'], current_data['tot_en'], '--*',
                             label=i, color = np.random.rand(3,))
        labels.append(labelpm)


    ax.legend(handles=labels)
    plt.show()

def plot_all(path):
    path = path[0]
    f = open(path, 'r')
    names = f.readlines()
    plot(names)


def get_cutoff(number_str):

    digits = [int(s) for s in number_str if s.isdigit()]
    cutoff = 0

    if 'Diborane' in number_str:
        digits = digits[1:]

    n = len(digits)

    for i in range(n):
        cutoff += digits[i] * 10**(n - 1 - i)
    return cutoff


def get_name(path):
    full_name = path.split('/')[-1]
    end_pos = 0
    for i in range(len(full_name)):
        if full_name[i].isdigit():
            end_pos = i-1
    return full_name[:end_pos].replace(' ', '')


if __name__ == "__main__":

    if sys.argv[1] == 'prepare':
        prepare(sys.argv[2:])

    elif sys.argv[1] == 'plot':
        plot(sys.argv[2:])
    elif sys.argv[1] == 'plot_all':
        plot_all(sys.argv[2:])
