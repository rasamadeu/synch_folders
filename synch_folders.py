#!/usr/bin/python3

import sys
import argparse
import os
from time import sleep

import directory as dir
# Look at argparse module to handle command line arguments at https://docs.python.org/3/library/argparse.html


def main():

    args = sys.argv[1:]
    if len(args) != 4:
        print("Wrong number of inputs")
        print("usage: synch_folders source_folder replica_folder time_delta_sec log_file")
        return

    src = args[0]
    replica = args[1]

    # Create
    src_dir = dir.Directory(src)
    replica_dir = dir.Directory(src)
    print(src_dir)
    # replica_dir = dir.Directory(replica)

    return


if __name__ == "__main__":
    main()
