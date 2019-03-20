#!/usr/bin/env python3
import os


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
        print(next_char)
        file_relativepath += next_char
    file_relativepath = file_relativepath.lstrip()
    return sha1_hash_when_commit, file_relativepath


def update_current_info(descriptor, time, file_sha1_hash):
    """
    Write the current time and sha1 hash of a file to the index file.

    Input:
        - descriptor: a file descriptor, must point to the start of the index
        line
        - time: the formatted string represent mtime of the file
        - file_sha1_hash: the sha1 hash of the content of the file
        - filepath: path to the current file
    """
    if file_sha1_hash == "":
        print("updating files failed")
    # Convert the modification time of the file to string
    time = convert_mtime_to_formatted_string(current_path)
    # Write down the timestamp
    os.write(descriptor, bytes(time, encoding="utf-8"))
    os.write(descriptor, b" ")
    # Write down the current sha1 code of the content of the file.
    os.write(descriptor, bytes(file_sha1_hash, encoding="utf-8"))
    os.write(descriptor, b" ")


def update_commit_info(descriptor, file_sha1_hash):
    """
    Update the commit sha1 code of a file in index

    Input:
        - descriptor: a file descriptor. Point to the start of the commit sha1
        field
        - file_sha1_hash: the sha1 code of the file, taken from the add sha1
        field in the index
    """
    if file_sha1_hash:
        os.write(descriptor, bytes(file_sha1_hash, encoding="utf-8"))
    else:
        blank = "                                        "
    os.write(descriptor, b" ")


def update_file_path(descriptor, current_path):
    """
    Update the filename in index

    Input:
        - descriptor: a file descriptor. Point to the start of the filename
        field
        - current_path: relative path of the file from the lgit repository
    """
    os.write(descriptor, bytes(current_path, encoding="utf-8"))
    os.write(descriptor, b"\n")
