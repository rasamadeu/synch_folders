# synch_folders

A Python program that synchronizes two folders: source and replica. The program maintains a full, identical copy of source at replica folder. The synchronization is performed periodically, and the operations messages are printed to the console and logged to a file.
To run the program, you must have a Python interpreter (version 3.10 or higher).

# Usage

```
python3 synch_folders.py [-h] [-s] source replica time_delta log_file
```

## Positional arguments:
| Argument  | Description |
| :-------: | :---------: |
| source    | The path of the folder to be copied |
| replica   | The path of the folder which stores the copy |
| time_delta| The time interval in seconds between synchronizations |
| log_file  | The file containing the log messages of the program |

## Options:
| Argument     | Description |
| :---------:  | :---------: |
| -h, --help   | show this help message and exit |
| -s, --shallow| Option that sets shallow file comparison ON.|

## Shallow mode:
- ON: Files' metadata (file type, size and modification time) is compared.
- OFF: Files' content is compared via MD5 hashing.

> [!IMPORTANT]
> The program is prepared to deal with changes in replica content in between synchronizations, if for some reason someone altered its contents. However, if replica is changed during the synchronization, the program might crash.
> If you guarantee that the replica folder is not changed by anyone other than the program, you can optimise the synch_folders.py by moving line 94:
>```
>    replica_dir = dir.Directory(replica, shallow=args["shallow"])
>```
> before the while loop.




