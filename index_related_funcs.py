#!/usr/bin/env python3
import os
from os import lseek, pwrite, path


def get_index_dictionary(parent_dir):
    """
    Get a dictionary contains the infos on each line of the index file.

    Input:
        - parent_dir: the directory that contains the lgit repository

    Output:
        - index_dict: A dictionary, with key is the relative file path of the
        file, the value is a tuple contains its info inside the index file and
        the length of the previous line.
    """
    # Open the index file
    try:
        index_file = open(path.join(parent_dir, ".lgit/index"), "r+")
    except PermissionError as e:
        print(e.filename + ":", "index file open failed: PermissionDenied")
        return None
    # Save its content
    content = index_file.readlines()
    # Split each line of the content into multiple fields
    index_info_list = [(index_line[:14],
                        index_line[15:55],
                        index_line[56:96],
                        index_line[97:137],
                        index_line[138:-1])
                       for index_line in content]
    # Create the dictionary
    index_dict = {index_info[4]: (index_info, (len(content[order - 1])
                                               if order - 1 >= 0
                                               else 0))
                  for order, index_info in enumerate(index_info_list)}
    return index_dict


def get_line_position(index_dict, file_path):
    """
    Get the position of the line for that file path in the index file.

    Input:
        - index_dict: A dictionary returned by the get_index_dictionary
        functions
        - file_path: The relative path of the file from the lgit repository
    """
    position = 0
    for index, key_name in enumerate(index_dict.keys()):
        if key_name == file_path:
            break
        else:
            position += index_dict[key_name][1]
    return position


def read_index_file(descriptor):
    """
    Read a line in the index file

    Input:
        - descriptor: a file descriptor. Must point to the start
        of the line

    Ouput:
        A tuple containing:
        - timestamp: the timestamp of the current file
        - current_sha1: the hash SHA1 of the current file
        - sha1_hash_when_add: the hash SHA1 when the file is added
        - sha1_hash_when_commit: the hash SHA1 when the file is committed
        - file_relativepath: the relative path to the file from the current
        directory
    """
    timestamp = os.read(descriptor, 14)
    current_sha1_hash = os.read(descriptor, 41).decode().lstrip()
    sha1_hash_when_add = os.read(descriptor, 41).decode().lstrip()
    sha1_hash_when_commit, file_relativepath = read_commit_and_path(descriptor)
    return (timestamp, current_sha1_hash, sha1_hash_when_add,
            sha1_hash_when_commit, file_relativepath)


def read_commit_and_path(descriptor):
    """
    Read the commit hash and relative path from index file or snapshot
    object.

    Input:
        - descriptor: a file descriptor. Must point at the start of the
        sha1 hash when commit

    Output:
        - sha1_hash_when_commit: the hash SHA1 when the file is committed
        - file_relativepath: the relative path to the file from the current
    """
    sha1_hash_when_commit = os.read(descriptor, 41).decode().lstrip()
    file_relativepath = ""
    next_char = os.read(descriptor, 1).decode()
    while next_char != "\n" and next_char != "":
        next_char = os.read(descriptor, 1).decode()
        file_relativepath += next_char
    file_relativepath = file_relativepath.lstrip()
    return sha1_hash_when_commit, file_relativepath


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
    Update certain field on the index line of a file, then return the
    descriptor back to the start of the line

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
    if not isinstance(content, bytes):
        os.pwrite(descriptor, bytes(content, encoding="utf-8"),
                  offsetDict[field])
    else:
        os.pwrite(descriptor, content,
                  offsetDict[field])
    os.lseek(descriptor, -(offsetDict[field] - len(content)), 1)


def read_certain_field_of_index(descriptor, field):
    """
    Read a certain field of the index line, then return the descriptor back to
    the start of the line

    Input:
        - descriptor: a file descriptor, must point to the start of the index
        line
        - field: ranging from 0 to 5, represent which field will be read. 5
        will be reading the whole line.
    """
    # Dictionary contains the offset of each field, counting from the start
    # of the line
    offsetDict = {0: 0, 1: 15, 2: 56, 3: 97, 4: 138}
    length = {0: 14, 1: 40, 2: 40, 3: 40}
    os.lseek(descriptor, offsetDict[field])
    if field != 4:
        return os.read(descriptor, length[field])
    else:
        file_path = os.read(descriptor, 1)
        next_char = 1
        while next_char != "\n" and next_char:
            next_char = os.read(descriptor, 1)
            file_path += next_char
        return file_path
