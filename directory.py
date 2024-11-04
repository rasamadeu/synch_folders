import os
import shutil
import pdb


class File:
    def __init__(self, filename):
        self.__filename = filename
        # self.__hash = hash

    def get_filename(self):
        return self.__filename


class Directory:

    def __init__(self, path: str, root_path=""):
        if not root_path:
            self.__root_path = path
            self.__rel_path = ""
        else:
            self.__root_path = root_path
            self.__rel_path = path
        self.__dirs = dict()
        self.__files = dict()

        cur_path = self.__root_path + self.__rel_path
        content = os.listdir(cur_path)
        # Recursive creation of Directory
        for f in content:
            if os.path.isdir(cur_path + "/" + f):
                self.__dirs[f] = Directory(
                    self.__rel_path + "/" + f,
                    self.__root_path
                )
            else:
                self.__files[f] = File(f)

    def get_dir_path(self) -> str:
        return self.__root_path + self.__rel_path + '/'

    def get_files(self) -> dict():
        return self.__files

    def get_dirs(self) -> dict():
        return self.__dirs

    # Synchs this directory to exactly match source Directory
    def synch(self, source) -> None:
        source_files = source.get_files()
        source_dirs = source.get_dirs()
        dirpath = self.get_dir_path()

        # Remove files from replica dir that are not in source dir
        for filename in self.__files:
            if filename not in source_files:
                os.remove(dirpath + filename)
                self.__files.remove(filename)

        # Create exact copy of files of source dir in replica dir
        for filename in source_files:
            if filename in self.__files:
                pass
            else:
                origin = dirpath + filename
                dest = self.get_dir_path() + filename
                os.copy2(origin, dest)
                self.__files.add(filename)

        # Remove dirs from replica dir that are not in source dir
        for dirname in self.__dirs:
            if dirname not in source_dirs:
                shutil.rmtree(dirpath + dirname)
                self.__dirs.remove(dirname)

        # Create exact copy of dirs of source dir in replica dir
        for filename in source_files:
            if filename in self.__files():
                pass
            else:
                origin = dirpath + dirname
                dest = self.get_dir_path() + dirname
                os.copytree(origin, dest)
                self.__dirs.add(dirname)

    # Returns a string with the directory tree
    def ls_dir(self, offset=""):
        print_str = (f"{offset}dir: {self.get_dir_path()}\n")
        for file in sorted(list(self.__files.keys())):
            print_str += f"{offset}  f: {file}\n"
        for dir in sorted(list(self.__dirs.keys())):
            print_str += self.__dirs[dir].ls_dir(offset + "  ")
        return print_str

    def __str__(self):
        # Remove last \n
        return self.ls_dir()[:-1]
