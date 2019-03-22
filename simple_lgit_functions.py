#!/usr/bin/env python3
import os
from index_related_funcs import *
from os import mkdir, environ, path


def init_lgit(init_path="."):
    """
    Initialize the directories structure
    """
    current_dir_path = path.abspath(init_path)
    # Create lgit directory
    try:
        mkdir(".lgit")
        print("Initialize empty lgit repository in",
              path.join(current_dir_path, ".lgit"))
    except FileExistsError:
        print("Reinitialized existing Git repository in",
              path.join(current_dir_path, ".lgit"))
        pass
    except PermissionError:
        print(current_dir_path + "/.lgit: PermissionDenied")
        return
    except FileNotFoundError:
        print("Cannot find", current_dir_path)
        return
    # Dictionary contains all the other paths for the directory structure
    dir_path_list = [".lgit/objects", ".lgit/commits", ".lgit/snapshots"]
    for dir_path in dir_path_list:
        try:
            mkdir(path.join(current_dir_path, dir_path))
        except FileExistsError:
            pass
    # Create index file
    index = open(path.join(current_dir_path, ".lgit/index"), "w+")
    # Create config file, write the user name on it
    config = open(path.join(current_dir_path, ".lgit/config"), "w+")
    # Write the username to the config file
    config.write(environ.get("LOGNAME"))
    index.close()
    config.close()


def config_lgit(args, parent_dir):
    """
    Configurate the author's name in the config file

    Input:
        - args: the arguments that were parsed by the parser
        - parent_dir: the directory that contains the lgit repository
    """
    config_file_path = path.join(parent_dir, ".lgit/config")
    # Open the config file
    try:
        config_file = open(config_file_path, "w+")
        # Write the new author's name to the config file
        config_file.write(args.author)
    except PermissionDenied:
        print("Unable to access", config_file_path)


def list_files_lgit(args, parent_dir):
    """
    List the files that are being tracked by lgit, relative to the current
    directory

    Input:
        - args: the arguments that were parsed by the parser
        - parent_dir: the directory that contains the lgit repository
    """
    # Get the index dictionary
    index_dict = get_index_dictionary(parent_dir)
    # If it is empty (whether because of error or the file is empty), return
    if not index_dict:
        return
    # Get the files that are relative to the current directory from the
    # dictionary
    tracking_path_list = ["%s/%s" % (parent_dir, infos[4])
                          for infos in index_dict.values()
                          if path.abspath(".")
                          in path.dirname("%s/%s" % (parent_dir, infos[4]))
                          and path.isfile("%s/%s" % (parent_dir, infos[4]))]
    # Print their path
    for file_path in tracking_path_list:
        print(path.relpath(file_path))
