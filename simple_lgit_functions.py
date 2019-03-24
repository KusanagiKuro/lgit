#!/usr/bin/env python3
import os
from index_related_funcs import *
from os import mkdir, environ, path, getcwd
from os.path import join, dirname, isfile, relpath


def init_lgit():
    """
    Initialize the directories structure
    """
    current_dir_path = getcwd()
    # Create lgit directory in the current directory
    try:
        mkdir(".lgit")
    except FileExistsError:
        print("Git repository already initialized.")
    except PermissionError:
        print(current_dir_path + "/.lgit: PermissionDenied")
        return
    except FileNotFoundError:
        print("Cannot find", current_dir_path)
        return
    # List contains all the other paths for the directory structure
    dir_path_list = [".lgit/objects", ".lgit/commits", ".lgit/snapshots"]
    for dir_path in dir_path_list:
        try:
            mkdir(join(current_dir_path, dir_path))
        except FileExistsError:
            pass
    # Create index file
    index = open(join(current_dir_path, ".lgit/index"), "w+")
    # Create config file, write the user name on it
    config = open(join(current_dir_path, ".lgit/config"), "w+")
    # Write the username to the config file
    config.write(environ.get("LOGNAME") + "\n")
    index.close()
    config.close()


def config_lgit(args, parent_dir):
    """
    Configurate the author's name in the config file

    Input:
        - args: the arguments that were parsed by the parser
        - parent_dir: the directory that contains the lgit repository
    """
    config_file_path = join(parent_dir, ".lgit/config")
    # Open the config file
    try:
        config_file = open(config_file_path, "w+")
        # Write the new author's name to the config file
        config_file.write(args.author[0] + "\n")
    except PermissionError:
        return
