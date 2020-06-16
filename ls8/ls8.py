#!/usr/bin/env python3

"""Main."""

import sys
from os import listdir
from cpu import *

cpu = CPU()
# create a dictionary of files in examples folder
files = {f: None for f in listdir("examples")}

# if filename is provided in cmd line
if len(sys.argv) > 1:
    filename = sys.argv[1]

    # check if filename provided is valid
    if filename in files:
        cpu.load(filename)
    else:
        print(f"Invalid Filename")
        sys.exit(1)


else:
    # load print8 as default file
    cpu.load("print8.ls8")
