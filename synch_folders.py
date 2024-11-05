#!/usr/bin/python3

import sys
import os
import shutil
import argparse
from time import sleep

import directory as dir
# Look at argparse module to handle command line arguments at https://docs.python.org/3/library/argparse.html


def main():

    args = sys.argv[1:]
    if len(args) != 4:
        print("Wrong number of inputs")
        print("usage: synch_folders source_folder replica_folder time_delta_sec log_file")
        return

    source = args[0]
    replica = args[1]

    # Instantiate Directory objects for source and replica

    i = 1
    while True:
        source_dir = dir.Directory(source, shallow=True)
        replica_dir = dir.Directory(replica, shallow=True)
        os.system('clear')
        print(source_dir)
        print(i)
        print(replica_dir)
        i += 1
        replica_dir.synch(source_dir)
        sleep(10)
    return


if __name__ == "__main__":
    main()
