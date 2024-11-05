import filecmp
import hashlib
import os
import shutil
import pdb
from datetime import datetime


# Append to log_file the log_message
def store_log_message(log_file, log_message):
    with open(log_file, 'a') as f:
        f.write(log_message + "\n")


class File:
    def __init__(self, filename, path, shallow=True):
        self.__filename = filename
        self.__path = path
        # shallow controls how we check if files are equal
        # shallow = True:
        # compare files metadata (file type, size and modification time)
        # shallow = False:
        # compare file content (with md5 hashing)
        self.__shallow = shallow
        if not self.__shallow:
            # Buffer with 4kB size
            BUF_SIZE = 4096
            hash = hashlib.md5()
            with open(self.get_path(), 'rb') as f:
                buf = f.read(BUF_SIZE)
                while buf:
                    hash.update(buf)
                    buf = f.read(BUF_SIZE)
            self.__hash = hash.hexdigest()

    def get_filename(self):
        return self.__filename

    def get_file_hash(self):
        return self.__hash

    def update_file_hash(self, file):
        if not self.__shallow:
            self.__hash = file.get_file_hash()

    def get_path(self):
        return self.__path + '/' + self.__filename

    def __eq__(self, file):
        if self.__shallow:
            return filecmp.cmp(self.get_path(), file.get_path())
        else:
            return self.get_file_hash() == file.get_file_hash()

    def __str__(self):
        return self.get_path()


class Directory:

    def __init__(self, path: str, shallow=True):

        # Step for better formatting of messages
        if path[-1] != "/":
            path += "/"

        self.__path = path
        self.__dirs = dict()
        self.__files = dict()
        # shallow controls how we check if files are equal
        self.__shallow = shallow

        # Recursive creation of Directory
        content = os.listdir(self.__path)
        for f in content:
            if os.path.isdir(self.__path + f):
                self.__dirs[f] = Directory(self.__path + f, self.__shallow)
            else:
                self.__files[f] = File(f, self.__path, self.__shallow)

    def get_dir_path(self) -> str:
        return self.__path

    def get_files(self) -> dict():
        return self.__files

    def get_dirs(self) -> dict():
        return self.__dirs

    # Log operation message
    def log_message(self, mode: str, fname: str, ftype: str, source_name: str) -> str:
        message = datetime.now().ctime()
        if ftype == "dir":
            fname = fname + "/"
        if mode == "CREATE":
            return message + f":  Create and Copy '{fname}' {ftype} from {source_name} in {self.get_dir_path()}"
        if mode == "COPY":
            return message + f":  Copy '{fname}' {ftype} from {source_name} to {self.get_dir_path()}"
        if mode == "DELETE":
            return message + f":  Delete '{fname}' {ftype} in {self.get_dir_path()}"

    # Synchs this directory to exactly match source Directory
    def synch(self, source, log_file) -> None:
        source_files = source.get_files()
        source_dirs = source.get_dirs()
        source_dirpath = source.get_dir_path()
        replica_dirpath = self.get_dir_path()

        # Remove files from replica dir that are not in source dir
        for filename in list(self.__files):
            if filename not in source_files:
                os.remove(replica_dirpath + filename)
                del self.__files[filename]
                log_msg = self.log_message(
                    "DELETE", filename, "file", source_dirpath)
                print(log_msg)
                store_log_message(log_file, log_msg)

        # Create exact copy of files of source dir in replica dir
        for filename in source_files:
            origin = source_dirpath + filename
            dest = replica_dirpath + filename
            if filename in self.__files:
                # Check if files are the same
                if not self.__files[filename] == source_files[filename]:
                    shutil.copy2(origin, dest)
                    self.__files[filename].update_file_hash(
                        source_files[filename])
                    log_msg = self.log_message(
                        "COPY", filename, "file", source_dirpath)
                    print(log_msg)
                    store_log_message(log_file, log_msg)
            else:
                shutil.copy2(origin, dest)
                self.__files[filename] = File(
                    filename, replica_dirpath, self.__shallow)
                log_msg = self.log_message(
                    "CREATE", filename, "file", source_dirpath)
                print(log_msg)
                store_log_message(log_file, log_msg)

        # Remove dirs from replica dir that are not in source dir
        for dirname in list(self.__dirs):
            if dirname not in source_dirs:
                shutil.rmtree(replica_dirpath + dirname)
                del self.__dirs[dirname]
                log_msg = self.log_message(
                    "DELETE", dirname, "dir", source_dirpath)
                print(log_msg)
                store_log_message(log_file, log_msg)

        # Create exact copy of dirs of source dir in replica dir
        for dirname in source_dirs:
            if dirname in self.__dirs:
                self.__dirs[dirname].synch(source_dirs[dirname], log_file)
            else:
                origin = source_dirpath + dirname
                dest = replica_dirpath + dirname
                shutil.copytree(origin, dest)
                self.__dirs[dirname] = Directory(
                    self.__path + dirname, self.__shallow)
                log_msg = self.log_message(
                    "CREATE", dirname, "dir", source_dirpath)
                print(log_msg)
                store_log_message(log_file, log_msg)

    # Returns a string with the directory tree
    def ls_dir(self, offset="") -> str:
        print_str = (f"{offset}dir: {self.get_dir_path().split('/')[-2]}/\n")
        for file in sorted(list(self.__files.keys())):
            print_str += f"{offset}  f: {file}\n"
        for dir in sorted(list(self.__dirs.keys())):
            print_str += self.__dirs[dir].ls_dir(offset + "  ")
        return print_str

    def __str__(self):
        # Remove last \n
        return self.ls_dir()[:-1]
