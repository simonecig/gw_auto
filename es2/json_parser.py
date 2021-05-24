#!/usr/bin/env python3

import json
import os
import sys

fname = "SSSP_efficiency.json"
f = open(fname)
parsed = json.load(f)


# Return cutoff value for
# the requested element.
# SSSP_efficiency.json must be
# present in the same folder as this
# module.
def cutoff(at_name):
    return parsed[at_name]["cutoff"]

# same as cutoff but for multiple
# elements
def cutoffs(at_names):
    values = []
    for name in at_names:
        values.append(parsed[name]["cutoff"])
    return values

