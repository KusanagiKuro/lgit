#!/usr/bin/env python3
import os
from os import lseek, pwrite, path
from os.path import join


def get_index_dictionary(parent_dir):
    """
    Get a dictionary contains the infos on each line of the index file.

    Input:
        - parent_dir: the directory that contains the lgit repository

    Output:
        - index_dict: A dictionary, with key is the relative file path of the
        file, the value is a tuple contains its info inside the index file and
        the line's position.
    """
    # Open the index file
    try:
        index_file = open(join(parent_dir, ".lgit/index"), "r+")
    except PermissionError as e:
        print(e.filename + ":", "index file open failed: PermissionDenied")
        return None
    # Save its content
    content = index_file.readlines()
    index_info_list = []
    char_count = 0
    # Split each line of the content into multiple fields
    for order, index_line in enumerate(content):
        index_info_list.append((index_line[:14],
                                index_line[15:55],
                                index_line[56:96],
                                index_line[97:137],
                                index_line[138:].strip(),
                                char_count))
        char_count += len(index_line)
    # Create the dictionary
    index_dict = {index_info[4]: index_info for index_info in index_info_list}
    return index_dict


def add_new_index(descriptor, time, file_sha1_hash, file_path):
    """
    Add new line to the index file

    Input:
        - descriptor: the file descriptor of the index file
        - time: the formatted string of the mtime for the newly added file
        - file_sha1_hash: the hash value of the file
        - file_path: the relative path of the file from the lgit repository
    """
    blank = "                                        "
    text = " ".join([time, file_sha1_hash, file_sha1_hash, blank, file_path])
    os.write(descriptor, bytes(text, encoding="utf-8"))
    os.write(descriptor, b"\n")


def update_file_index(descriptor, content, field):
    """
    Update certain field on the index line of a file

    Input:
        - descriptor: a file descriptor, must point to the start of the index
        line
        - content: the content of that we want to replace
        - field: ranging from 0 to 4, represent starting from which field
        that the index line should be overwritten.
    """
    # Dictionary contains the offset of each field, counting from the start
    # of the line
    offsetDict = {0: 0, 1: 15, 2: 56, 3: 97, 4: 138}
    try:
        if not isinstance(content, bytes):
            lseek(descriptor, offsetDict[field], 1)
            os.write(descriptor, bytes(content, encoding="utf-8"))
        else:
            lseek(descriptor, offsetDict[field], 1)
            os.write(descriptor, content)
    except TypeError:
        print("fatal: updating files failed.")
