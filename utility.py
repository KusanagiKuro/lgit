#!/usr/bin/env python3
import os
from hashlib import sha1
from os import path
from datetime import datetime


def handle_path(name, parent_dir):
    """
    Return a relative path from a parent dir
    """
    if name.startswith("~"):
        name = path.expanduser(name)
    else:
        name = path.abspath(name)
    return path.relpath(name, ".")


def read_and_hash(path):
    """
    Hash a content of a file using SHA1

    Input:
        - path: the path of the file

    Output:
        - The SHA1 hash code of the content, in binary form or normal form
        - The content of the file
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
    return hash.hexdigest(), file_content


def get_lgit_directory():
    """
    Get the closest directory that has a .lgit directory in it.
    """
    dirpath = path.abspath(".")
    while True:
        if path.exists(dirpath + "/.lgit") and path.isdir(dirpath + "/.lgit"):
            return dirpath
        elif dirpath == "/":
            print("fatal: not a git directory",
                  "(or any of the parentdirectories)")
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
    timestamp = datetime.fromtimestamp(path.getmtime(current_path))
    return datetime.strftime(timestamp, "%Y%m%d%H%M%S")
