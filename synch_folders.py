#!/usr/bin/python3

import argparse
import os
from time import sleep

import directory as dir


def check_source(source):
    if not os.path.isdir(source):
        raise Exception("The source path is not a valid directory path.")
    return source


def check_replica(replica, source):
    if replica == source:
        raise Exception(
            "The replica path must be different from the source path.")
    if os.path.isdir(replica):
        print("The replica path already exists.")
        print("Are you sure you want to proceed? Proceeding with the program will delete replica folder contents.")
        answer = input("Write [y]es or [n]o: ")
        while answer.lower() not in {"y", "n", "yes", "no"}:
            answer = input("Invalid answer: please write [y]es or [n]o: ")
        if answer.lower() in {"no", "n"}:
            raise Exception()
        return replica

    os.mkdir(replica)
    return replica


def check_time_delta(time_delta):
    time_delta_int = int(time_delta)
    if time_delta_int <= 0:
        raise ValueError
    return time_delta


def check_log_file(log_file):
    if os.path.isdir(log_file):
        raise Exception("log_file must contain a valid file path.")
    if os.path.isfile(log_file):
        print("The log_file already exists.")
        print("Are you sure you want to proceed? Proceeding with the program will delete log_file contents.")
        answer = input("Write [y]es or [n]o: ")
        while answer.lower() not in {"y", "n", "yes", "no"}:
            answer = input("Invalid answer: please write [y]es or [n]o: ")
        if answer.lower() in {"no", "n"}:
            raise Exception()

    # Clear the log_file content
    with open(log_file, "w") as f:
        f.write("")
    return log_file


def main():

    parser = argparse.ArgumentParser(
        description=("This program synchs two folders: source and replica.\n"
                     "Every time_delta seconds, the replica folder is updated to contain an exact copy of source.\n"
                     "Log messages are presented in the console and stored in log_file.")
    )
    parser.add_argument("source", help="The path of the folder to be copied")
    parser.add_argument(
        "replica", help="The path of the folder which stores the copy")
    parser.add_argument(
        "time_delta", help="The time interval in seconds between synchronizations")
    parser.add_argument(
        "log_file", help="The file containing the log messages of the program")
    parser.add_argument("-s", "--shallow",
                        help="Option that sets shallow file comparison ON.\nIf set, files metadata is compared instead of its content.",
                        action="store_false")

    args = vars(parser.parse_args())
    try:
        source = check_source(args["source"])
        replica = check_replica(args["replica"], args["source"])
        time_delta = check_time_delta(args["time_delta"])
        log_file = check_log_file(args["log_file"])
    except ValueError:
        print("time_delta must be a positive integer (seconds between synchronizations)")
        print("Program terminated.")
    except Exception as e:
        print(e)
        print("Program terminated.")

    while True:
        source_dir = dir.Directory(source, shallow=args["shallow"])
        replica_dir = dir.Directory(replica, shallow=args["shallow"])
        replica_dir.synch(source_dir, log_file)
        sleep(time_delta)
    return


if __name__ == "__main__":
    main()
