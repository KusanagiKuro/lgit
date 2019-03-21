#!/usr/bin/env python3
import os
from os import mkdir, environ, path, O_RDONLY, O_RDWR, O_CREAT, lseek
from index_related_funcs import *
from utility import *
from datetime import datetime


def add_lgit(args, parent_dir):
    """
    Process the arguments passed to the add command and execute the fitting
    function on each of them.

    Input:
        - args: the arguments parsed by the add command subparser
        - parent_dir: the directory that contains the lgit repository
    """
    # Convert all the name from the arguments to relative path
    path_list = [handle_path(name, parent_dir)
                 for name in args.filenames[::-1]]
    # Get the infos from the index file
    index_dict = get_index_dictionary(parent_dir)
    # Create a file descriptor for index file
    descriptor = os.open("./.lgit/index", os.O_WRONLY)
    while path_list:
        # Pop each path and execute the fitting function
        current_path = path_list.pop()
        # If the path doesn't exist, print an error message
        if not path.exists(current_path):
            print("fatal:", current_path, "did not match any files")
        elif path.isfile(current_path):
            add_file(current_path, parent_dir, descriptor, index_dict)
        elif path.isdir(current_path):
            add_directory(current_path, parent_dir, path_list)
    # Close the file descriptor
    os.close(descriptor)


def add_file(current_path, parent_dir, descriptor, index_dict):
    """
    Add or update the sha1 hash of the file and its timestamp
    in the index file

    Input:
        - current_path: relative path of the file from the base directory
        - parent_dir: the directory that contains the lgit repository
        - index_dict: the dictionary contains all the infos inside the index
        file.
    """
    # Read file content and hash it
    file_sha1_hash, file_content = read_and_hash(current_path)
    # Convert the modification time of the file to string
    time = convert_mtime_to_formatted_string(current_path)
    # If the file is already tracked, update it
    if current_path in index_dict.keys():
        # If the file is already up to date, no need to rewrite.
        if (time == index_dict[current_path][0]
                and file_sha1_hash == index_dict[current_path][2]):
            return
        # Move the file descriptor to the correct position
        lseek(descriptor, index_dict[current_path][5], 0)
        # Update the timestamp. current sha1 hash, add sha1 hash
        update_file_index(descriptor, " ".join([time,
                                                file_sha1_hash,
                                                file_sha1_hash]), 0)
    else:
        lseek(descriptor, 0, 2)
        add_new_index(descriptor, time, file_sha1_hash, current_path)
    # Create the new directory + object file in objects if needed
    make_directory_and_object_file(file_sha1_hash, file_content, parent_dir)
    # Return the file descriptor to the start of the index file.
    lseek(descriptor, 0, 0)


def make_directory_and_object_file(file_sha1_hash, file_content, parent_dir):
    """
    Make the object directory and file for the adding file.

    Input:
        - file_sha1_hash: the hash of the content
        - file_content: the content of the file
        - parent_dir: the path to the lgit repository
    """
    # Create a path for the new directory, which is the first 2 characters
    # of the hash.
    new_dir_path = path.join(parent_dir, ".lgit/objects", file_sha1_hash[:2])
    # Create the directory
    try:
        mkdir(new_dir_path)
    except FileExistsError:
        pass
    new_file_path = path.join(new_dir_path, file_sha1_hash[2:])
    # Create the new file
    try:
        new_file = open(new_file_path, "wb+")
    except PermissionError:
        print("Cannot add an object to a lgit repository")
        return
    new_file.write(file_content)


def add_directory(current_path, parent_dir, path_list):
    """
    Walk through the directory and add all of its childs to the path list
    """
    try:
        for item in os.scandir(current_path):
            path_list.append(path.join(current_path, item.name))
    except PermissionError:
        pass
