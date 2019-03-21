#!/usr/bin/env python3
import os
from utility import try_and_pass_function
from index_related_funcs import *
from os import mkdir, environ


def init_lgit():
    """
    Initialize the directories structure
    """
    # Create lgit directory
    if try_and_pass_function(mkdir, FileExistsError, "./.lgit"):
        print("Initialize empty lgit repository in",
              path.join(path.abspath("."), ".lgit"))
    else:
        print("Reinitialized existing Git repository in",
              path.join(path.abspath("."), ".lgit"))
    # Create objects directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/objects")
    # Create commit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/commits")
    # Create snapshots directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/snapshots")
    # Create index file
    index = open("./.lgit/index", "w")
    # Create config file, write the user name on it
    config = open("./.lgit/config", "w")
    # Write the username to the config file
    config.write(environ.get("LOGNAME"))
    index.close()
    config.close()


def commit_lgit(args, parent_dir):
    pass


def remove_lgit(args, parent_dir):
    pass


def config_lgit(args, parent_dir):
    config_file_path = path.join(parent_dir, ".lgit/config")
    try:
        config_file = open(config_file_path, "w+")
    except PermissionDenied:
        print("Unable to access", config_file_path)
        return
    config_file.write(args.author)
    pass


def show_status_lgit(args, parent_dir):
    pass


def list_files_lgit(args, parent_dir):
    pass


def show_log_lgit(args, parent_dir):
    pass
