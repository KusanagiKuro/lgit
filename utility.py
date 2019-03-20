#!/usr/bin/env python3
import os
from hashlib import sha1
from os import path

def try_and_pass_function(function, error, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        pass


def handle_path(name, relative=False):
    """
    Return an absolute path
    """
    if name.startswith("~"):
        name = path.expanduser(name)
    if relative:
        return path.relpath(name)
    else:
        return path.abspath(name)


def hash_file_content(path, binary=False):
    hash = sha1()
    file = open(path, "rb")
    file_content = file.read()
    hash.update(file_content)
    if binary:
        return hash.digest()
    else:
        return hash.hexdigest()


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
        - file_relative_path: the relative path to the file from the current
        directory
    """
    timestamp = os.read(descriptor, 12)
    current_sha1_hash = os.read(descriptor, 41).decode()[1:]
    sha1_hash_when_add = os.read(descriptor, 41).decode()[1:]
    sha1_hash_when_commit, file_relative_path = read_commit_and_path(descriptor)
    return (timestamp, current_sha1_hash, sha1_hash_when_add,
            sha1_hash_when_commit, file_relative_path)


def read_commit_and_path(descriptor):
    """
    Read the commit hash and relative path from index file or snapshot
    object.

    Input:
        - descriptor: a file descriptor. Must point at the start of the
        sha1 hash when commit
    
    Output:
        - sha1_hash_when_commit: the hash SHA1 when the file is committed
        - file_relative_path: the relative path to the file from the current
    """
    sha1_hash_when_commit = os.read(descriptor, 41).decode().lstrip()
    file_relative_path = ""
    next_char = os.read(descriptor, 1).decode()
    while next_char != "\n":
        next_char = os.read(descriptor, 1).decode()
        file_relative_path += next_char
    file_relative_path = file_relative_path[1:]
    return sha1_hash_when_commit, file_relative_path


def check_permission(filepath):
    return True
