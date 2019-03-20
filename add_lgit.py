#!/usr/bin/env python3
import os
from os import mkdir, environ, path, O_RDONLY, O_RDWR, O_CREAT, lseek
from utility import *
from index_related_funcs import *


def add_lgit(args, parent_dir):
    """
    Process the arguments passed to the add command and execute the fitting
    function on each of them.

    Input:
        - args: the arguments parsed by the add command subparser
    """
    # If the current directory doesn't have .lgit directory, raise error
    if not check_lgit_directory():
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    # Convert all the name from the arguments to relative path
    path_list = [handle_path(name, parent_dir)
                 for name in args.filenames[::-1]]
    while path_list:
        # Pop each of path and execute the fitting function
        current_path = path_list.pop()
        if path.isfile(current_path):
            add_file(current_path)
        elif path.isdir(current_path):
            add_directory(current_path, path_list)
        # If the path doesn't exist, print a warning message
        else:
            print("fatal:", current_path, "did not match any files")


def add_file(current_path):
    """
    Add or update the sha1 hash of the content in the file to the index file

    Input:
        - current_path: relative path of the file from the base directory
    """
    if not path_check(current_path, "r"):
        return
    infos, descriptor = is_file_in_index(current_path)
    if not infos and not descriptor:
        return
    # Create the new directory + object file in objects if needed
    file_sha1_hash = make_directory_and_object_file(current_path)
    if infos:
        lseek(descriptor, 1, -(138 + len(infos[5])))
        # If the sha1 code and mtime of current file and inside the index
        # are the same, stop
        if (time == infos[0] and file_sha1_hash == infos[2] and
                file_sha1_hash == infos[1]):
            return
    # Write down the new mtime and sha1 hash code
    update_current_info(descriptor, time, file_sha1_hash)
    # Write down the new sha1 hash code into the add hash field
    update_add_info(descriptor, current_path, file_sha1_hash)
    # If the file doesn't exist in the index file, write down commit and
    # relative filepath
    if not infos:
        update_commit_info(descriptor, None)
        update_file_path(descriptor, current_path, current_path)
    # Close the file descriptor
    descriptor.close()


def is_file_in_index(filepath):
    """
    Check if the line that lists the file path in an index file

    Input:
        - filepath: the relative path of the file

    Output:
        - infos: the infos that we got from index file. Will be None if some
          errors happens or no line is found.
        - descriptor: a file descriptor at the start of the line that has the
          name of the file. Will be None if some errors happens.
    """
    # Open the index file, raise erorr if needed
    try:
        descriptor = os.open("./.lgit/index", os.OS_RDWR | os.OS_CREAT)
    except PermissionError:
        descriptor = None
        print("Cannot open index file: PermissionDenied")
        return None, None
    # Read each line of the index file, stop if the file path is found or EOF
    infos = read_index_file(file)
    while filepath not in infos and infos != "":
        infos = read_index_file(file)
    # If the file is in the index file, return its info and the descriptor
    if infos:
        return infos, descriptor
    else:
        return None, descriptor


def make_directory_and_object_file(current_path):
    pass


def add_directory(current_path, path_list):
    pass
