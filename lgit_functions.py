#!/usr/bin/env python3
from os import mkdir, environ, path
from utility import try_and_pass_function


def init_lgit(args):
    """
    Initialize the directories structure
    """
    # Create lgit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit")
    # Create objects directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/objects")
    # Create commit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/commmits")
    # Create snapshots directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/snapshots")
    # Create index file
    index = open("./.lgit/index", "w")
    # Create config file, write the user name on it
    config = open("./.lgit/config", "w")
    config.write(environ.get("USER"))
    index.close()
    config.close()


def check_lgit_directory(args):
    """
    Check if the working directory has a lgit directory in it or not.
    """
    return path.exist("./.lgit")


def add_lgit(args):
    if not check_lgit_directory:
        print("fatal: not a git directory (or any of the parentdirectories)")
        return
    pass


def commit_lgit(args):
    pass


def remove_lgit(args):
    pass


def config_lgit(args):
    pass


def show_status_lgit(args):
    pass


def list_files_lgit(args):
    pass


def show_log_lgit(args):
    pass
