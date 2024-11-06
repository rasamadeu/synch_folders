# synch_folders

A Python program that synchronizes two folders: source and replica. The program maintains a full, identical copy of source at replica folder.
To run the program, you must have a Python interpreter (version 3.10 or higher).

# Usage

```
python3 synch_folders.py [-h] [-s] source replica time_delta log_file
```

## positional arguments:
- source         The path of the folder to be copied
- replica        The path of the folder which stores the copy
- time_delta     The time interval in seconds between synchronizations
- log_file       The file containing the log messages of the program

## options:
- -h, --help     show this help message and exit
- -s, --shallow  Option that sets shallow file comparison ON. If set, files
                 metadata is compared instead of its content.


