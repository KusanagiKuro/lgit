#!/usr/bin/env python3
import os
from hashlib import sha1
from os import path
from datetime import datetime


def handle_path(name):
    """
    Return a relative path from a parent dir
    """
    if name.startswith("~"):
        name = path.expanduser(name)
    else:
        name = path.abspath(name)
    return path.relpath(name, ".")


def read_and_hash(file_path, is_content_needed=True):
    """
    Hash a content of a file using SHA1

    Input:
        - file_path: the path of the file
        - is_content_needed: a boolean that decide whether the content needs to
        be returned.

    Output:
        - The SHA1 hash code of the content, in binary form or normal form
        - The content of the file
    """
    # Create the hash
    hash = sha1()
    # Open and read file content
    try:
        file = open(file_path, "rb")
    except PermissionError:
        print("error: open(\"%s\"): PermissionDenied" % file_path)
        return None, None
    except NotADirectoryError:
        print("error: open(\"%s\"): NotADirectoryError" % file_path)
        return None, None
    file_content = file.read()
    file.close()
    # Update it to the hash
    hash.update(file_content)
    # Return hash value and content if needed
    if is_content_needed:
        return hash.hexdigest(), file_content
    else:
        return hash.hexdigest()


def get_lgit_directory():
    """
    Get the closest directory that has a .lgit directory in it.
    """
    dir_path = os.getcwd()
    while dir_path != "/":
        if path.isdir(dir_path + "/.lgit"):
            return dir_path
        dir_path = path.dirname(dir_path)
    return None


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
