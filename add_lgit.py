#!/usr/bin/env python3
import os
from os import mkdir, environ, path, O_RDONLY, O_RDWR, O_CREAT, lseek, scandir
from os.path import basename, isfile, isdir, relpath, abspath, exists, join
from index_related_funcs import *
from utility import *
from datetime import datetime
from error import pathspec_error


def add_lgit(args, parent_dir):
    """
    Process the arguments passed to the add command and execute the fitting
    function on each of them.

    Input:
        - args: the arguments parsed by the add command subparser
        - parent_dir: the directory that contains the lgit repository
    """
    # Convert all the name from the arguments to relative path
    path_list = [handle_path(name) for name in args.filenames[::-1]]
    # Get the infos from the index file
    index_dict = get_index_dictionary(parent_dir)
    if index_dict is None:
        return
    # Create a file descriptor for index file
    index_file_path = join(parent_dir, ".lgit/index")
    descriptor = os.open(index_file_path, os.O_WRONLY)
    while path_list:
        # Pop each path and execute the fitting function
        current_path = path_list.pop()
        # If the path doesn't exist, print an error message
        if not exists(current_path):
            pathspec_error(current_path)
        elif basename(current_path) == ".lgit":
            continue
        elif isfile(current_path):
            add_file(current_path, parent_dir, descriptor, index_dict)
        elif isdir(current_path):
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
    mtime = convert_mtime_to_formatted_string(current_path)
    # Get the relative path from the repository
    rel_path_from_repository = relpath(abspath(current_path), parent_dir)
    try:
        update_info_when_add(descriptor, rel_path_from_repository,
                             mtime, file_sha1_hash, index_dict)
    except TypeError:
        print("error: unable to index file %s" % basename(current_path))
    # Create the new directory + object file in objects if needed
    make_directory_and_object_file(file_sha1_hash, file_content, parent_dir)
    # # Return the file descriptor to the start of the index file.
    # lseek(descriptor, 0, 0)


def update_info_when_add(descriptor, rel_path_from_repository,
                         mtime, file_sha1_hash, index_dict):
    """
    Update the index file when adding file

    Input:
        - descriptor: a file descriptor
        - rel_path_from_repository: the relative path of the file from the
        lgit repository
        - mtime: modification time of the file
        - file_sha1_hash: the hash of the content
        - index_dict: the dictionary contains all the infos inside the index
        file.
    """
    # If the file is already tracked, update it
    if rel_path_from_repository in index_dict.keys():
        # If the file is already up to date, no need to rewrite.
        if (mtime == index_dict[rel_path_from_repository][0]
                and
                file_sha1_hash == index_dict[rel_path_from_repository][2]):
            return
        # Move the file descriptor to the correct position
        lseek(descriptor, index_dict[rel_path_from_repository][5], 0)
        # Update the timestamp. current sha1 hash, add sha1 hash
        update_file_index(descriptor, " ".join([mtime,
                                                file_sha1_hash,
                                                file_sha1_hash]), 0)
    else:
        lseek(descriptor, 0, 2)
        add_new_index(descriptor, mtime, file_sha1_hash,
                      rel_path_from_repository)


def make_directory_and_object_file(file_sha1_hash, file_content, parent_dir):
    """
    Make the object directory and file for the adding file.

    Input:
        - file_sha1_hash: the hash of the content
        - file_content: the content of the file
        - parent_dir: the path to the lgit repository
    """
    try:
        # Create a path for the new directory, which is the first 2 characters
        # of the hash.
        new_dir_path = join(parent_dir, ".lgit/objects", file_sha1_hash[:2])
        # Create the directory
        try:
            mkdir(new_dir_path)
        except FileExistsError:
            pass
        new_file_path = join(new_dir_path, file_sha1_hash[2:])
        # Create the new file
        try:
            new_file = open(new_file_path, "wb+")
        except PermissionError:
            print("Cannot add an object to a lgit repository")
            return
        new_file.write(file_content)
    except TypeError:
        print("fatal: updating files failed")


def add_directory(current_path, parent_dir, path_list):
    """
    Walk through the directory and add all of its childs to the path list

    Input:
        - current_path: relative path of the file from the base directory
        - parent_dir: the directory that contains the lgit repository
        - path_list: the list of paths that will be checked by the add command
    """
    try:
        for item in scandir(current_path):
            path_list.append(join(current_path, item.name))
    except PermissionError:
        pass
