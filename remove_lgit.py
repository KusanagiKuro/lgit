#!/usr/bin/env python3
import os
from os import path
from os.path import relpath, abspath, exists, isfile
from utility import handle_path, read_and_hash
from index_related_funcs import get_index_dictionary
from error import *


def remove_lgit(args, parent_dir):
    # Convert all the name from the arguments to relative path
    path_list = [handle_path(name) for name in args.filenames[::-1]]
    # Get the infos from the index file
    index_dict = get_index_dictionary(parent_dir)
    if index_dict is None:
        return
    # The list contains removed_files
    removed_files = []
    # Pop each path out of the list and process it.
    while path_list:
        current_path = path_list.pop()
        if not exists(current_path):
            pathspec_error(current_path)
        elif isfile(current_path):
            remove_file(current_path, parent_dir, index_dict, removed_files)
        else:
            print("fatal: not removing '%s' recursively without -r"
                  % current_path)
    # Rewrite the index file if there is any file that got successfully removed
    if removed_files:
        rewrite_index_file(removed_files, index_dict, parent_dir)


def remove_file(file_path, parent_dir, index_dict, removed_files):
    """
    Remove a file from the index

    Input:
        - file_path: the path of the file
        - index_dict: the dictionary contains all the infos inside the index
        file.
        - parent_dir: the directory that contains the lgit repository
        - removed_files: the list contains all previously removed files.
    """
    # The relative path of the file from the lgit repository
    rel_path_from_repository = relpath(abspath(file_path), parent_dir)
    # Check for the error
    if check_error_when_removing(index_dict, rel_path_from_repository):
        return
    # Delete the original file and recursively delete its parent directory if
    # they are empty
    try:
        delete_original_file(file_path, parent_dir)
    except PermissionError:
        print("fatal: lgit rm: '%s': Permission denied")
    # Add the removed file to the list
    removed_files.append(rel_path_from_repository)
    return


def check_error_when_removing(index_dict, rel_path_from_repository):
    """
    Check if the process of removing file has any error

    Input:
        - index_dict: the dictionary contains all the infos inside the index
        file.
        - rel_path_from_repository: The relative path of the removed file from
        the lgit repository
    """
    # If the file path isn't in index, raise error
    if rel_path_from_repository not in index_dict.keys():
        pathspec_error(file_path)
        return True
    return False


def delete_original_file(file_path, parent_dir):
    """
    Delete the original file and recursively delete its parent directory if
    they are empty

    Input:
        - file_path: path of the file that needs to be deteled
        - parent_dir: the directory that contains the lgit repository
    """
    # Delete the original file
    os.remove(file_path)
    directory = path.abspath(".")
    # Recursively delete the parent directory if they are empty
    while not os.listdir(directory):
        os.rmdir(directory)
        directory = path.dirname(directory)


def rewrite_index_file(removed_files, index_dict, parent_dir):
    """
    Rewrite the index file after the removal

    Input:
        - removed_files: List of removed files
        - index_dict: the dictionary contains all the infos inside the index
        file.
        - parent_dir: the directory that contains the lgit repository
    """
    new_index_content = "\n".join([" ".join(infos[:5]) for rel_path, infos
                                   in index_dict.items()
                                   if rel_path not in removed_files])
    index_file = open("%s/.lgit/index" % parent_dir, "w+")
    index_file.write(new_index_content + "\n")
    index_file.close()
