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
    index_info_list = []
    char_count = 0
    # Split each line of the content into multiple fields
    for order, index_line in enumerate(content):
        index_info_list.append((index_line[:14],
                                index_line[15:55],
                                index_line[56:96],
                                index_line[97:137],
                                index_line[138:-1],
                                char_count))
        char_count += len(index_line)
    # Create the dictionary
    index_dict = {index_info[4]: index_info for index_info in index_info_list}
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
            position += index_dict[key_name][5]
    return position


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
    if not isinstance(content, bytes):
        os.lseek(descriptor, offsetDict[field], 1)
        os.write(descriptor, bytes(content, encoding="utf-8"))
    else:
        os.lseek(descriptor, offsetDict[field], 1)
        os.write(descriptor, content)


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
    lseek(descriptor, offsetDict[field])
    if field != 4:
        return os.read(descriptor, length[field])
    else:
        file_path = os.read(descriptor, 1)
        next_char = 1
        while next_char != "\n" and next_char:
            next_char = os.read(descriptor, 1)
            file_path += next_char
        return file_path
