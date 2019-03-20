#!/usr/bin/env python3
import os
from hashlib import sha1
from os import path


def try_and_pass_function(function, error, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        pass


def handle_path(name, parent_dir, absolute=False):
    """
    Return a relative path from a parent dir
    """
    if name.startswith("~"):
        name = path.expanduser(name)
    return path.relpath(name, parent_dir)


def hash_file_content(path, binary=False):
    """
    Hash a content of a file using SHA1

    Input:
        - path: the path of the file
        - binary: will the return value in binary form or not

    Output:
        - The SHA1 hash code of the content, in binary form or normal form
    """
    # Create the hash
    hash = sha1()
    # Open and read file content
    file = open(path, "rb")
    file_content = file.read()
    file.close()
    # Update it to the hash
    hash.update(file_content)
    # Return hash value
    if binary:
        return hash.digest()
    else:
        return hash.hexdigest()


def get_lgit_directory():
    """
    Get the closest directory that has a .lgit directory in it.
    """
    dirpath = path.abspath(".")
    while True:
        if path.exists(dirpath + "/.lgit") and path.isdir(dirpath + "/.lgit"):
            return path
        elif dirpath == "/":
            return None
        else:
            dirpath = path.split(dirpath)[0]


def convert_mtime_to_formatted_string(current_path):
    """
    Convert the modification time of the file to formatted string

    Input:
        - current_path: relative path of the file

    Output:
        - timestamp_string: the 14-character string represent year, month, day,
        hour, minute, second
    """
    timestamp = path.getmtime(current_path)
    return datetime.strftime("%Y%m%d%H%M%S", timestamp)
