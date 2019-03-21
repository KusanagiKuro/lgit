#!/usr/bin/env python3
import os
from index_related_funcs import *
from os import mkdir, environ, path


def init_lgit():
    """
    Initialize the directories structure
    """
    # Create lgit directory
    try:
        mkdir(".lgit")
        print("Initialize empty lgit repository in",
              path.join(path.abspath("."), ".lgit"))
    except FileExistsError:
        print("Reinitialized existing Git repository in",
              path.join(path.abspath("."), ".lgit"))
        pass
    except PermissionError:
        print(os.path.abspath(".") + "/.lgit: PermissionDenied")
        return
    # Dictionary contains all the other paths for the directory structure
    dir_path_list = ["./.lgit/objects", "./.lgit/commits", "./.lgit/snapshots"]
    for dir_path in dir_path_list:
        try:
            mkdir(dir_path)
        except FileExistsError:
            pass
    # Create index file
    index = open("./.lgit/index", "w+")
    # Create config file, write the user name on it
    config = open("./.lgit/config", "w+")
    # Write the username to the config file
    config.write(environ.get("LOGNAME"))
    index.close()
    config.close()


def config_lgit(args, parent_dir):
    config_file_path = path.join(parent_dir, ".lgit/config")
    # Open the config file
    try:
        config_file = open(config_file_path, "w+")
    except PermissionDenied:
        print("Unable to access", config_file_path)
        return
    # Write the new author's name to the config file
    config_file.write(args.author)


def list_files_lgit(args, parent_dir):
    index_dict = get_index_dictionary(parent_dir)


def show_log_lgit(args, parent_dir):
    pass
