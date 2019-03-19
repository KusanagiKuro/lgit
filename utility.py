#!/usr/bin/env python3
from hashlib import sha1


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


def check_permission(filepath):
    return True
