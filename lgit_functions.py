#!/usr/bin/env python3
from os import mkdir, environ
from utility import try_and_pass_function


def init_lgit():
    """
    Initialize the directories structure
    """
    # Create lgit directory
    try_and_pass_function(mkdir, FileExistError, "./lgit")
    # Create objects directory
    try_and_pass_function(mkdir, FileExistError, "./lgit/objects")
    # Create commit directory
    try_and_pass_function(mkdir, FileExistError, "./lgit/commmits")
    # Create snapshots directory
    try_and_pass_function(mkdir, FileExistError, "./lgit/snapshots")
    # Create index file
    index = open("./lgit/index", "w")
    # Create config file, write the user name on it
    config = open("./lgit/config", "w")
    config.write(environ.get("USER"))
    index.close()
    config.close()


def add_lgit():
    pass


def commit_lgit():
    pass


def remove_lgit():
    pass


def configure_lgit():
    pass


def show_status_lgit():
    pass


def list_files_lgit():
    pass


def show_log_lgit():
    pass
