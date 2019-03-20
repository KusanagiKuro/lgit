#!/usr/bin/env python3
import os
from os import mkdir, environ, path, O_RDONLY, O_RDWR, O_CREAT
from utility import *


def init_lgit(args):
    """
    Initialize the directories structure
    """
    # Create lgit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit")
    # Create objects directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/objects")
    # Create commit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/commits")
    # Create snapshots directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/snapshots")
    # Create index file
    index = open("./.lgit/index", "w")
    # Create config file, write the user name on it
    config = open("./.lgit/config", "w")
    # Write the username to the config file
    config.write(environ.get("USER"))
    index.close()
    config.close()


def check_lgit_directory():
    """
    Check if the working directory has a lgit directory in it or not.
    """
    path = handle_path(".")
    while True:
        if path.exists(path + "/.lgit"):
            return True
        elif path == "/":
            break
        else:
            path = path.split(path)[0]
    return False


def add_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    path_list = [handle_path(name) for name in args.filenames[::-1]]
    while path_list:
        current_path = path_list.pop()
        if path.isfile(current_path):
            add_file(current_path)
        else:
            add_directory(current_path, path_list)
    pass


def add_file(current_path):
    pass


def is_file_in_index(filepath):
    """
    Check if the line that lists the file path in an index file

    Input:
        - filepath: the relative path of the file

    Output:
        - descriptor: a file descriptor at the start of the line that has the
          name of the file. Will be none if such line doesn't exist.
        - success: True if the function runs normally. False if something goes
          wrong
    """
    try:
        file = os.open("./.lgit/index", os.OS_RDWR)
    except PermissionError:
        descriptor = None
        print("Cannot open index file: PermissionDenied")
        return None, False
    line = read_index_file(file)
    while filepath not in line and line != None:
        pass
    pass


def add_directory(current_path, path_list):
    pass


def commit_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass


def remove_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass


def config_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass


def show_status_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass


def list_files_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass


def show_log_lgit(args):
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass
