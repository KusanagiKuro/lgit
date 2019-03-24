#!/usr/bin/env python3
import os
from os import path, O_RDWR, O_CREAT, O_WRONLY, listdir, getcwd
from os.path import join, isdir, isfile, relpath
from index_related_funcs import *
from datetime import datetime
from utility import read_and_hash, convert_mtime_to_formatted_string
from branch_related_funcs import get_current_branch


def has_any_commit(parent_dir):
    return listdir(join(parent_dir, ".lgit/snapshots"))


def get_status_lst(list_files, index_dict):
    """
    Get the lists that contains file paths for changes to be commit, changes
    not in commit and untracked file for status command.

    Input:
        - list_files: List of files in current working directory
        - index_dict: the dictionary contains all the infos inside the index
        file.
    """
    # List of files that are added but havent been committed
    in_commit_list = [file_path for file_path in index_dict.keys()
                      if index_dict[file_path][2] != index_dict[file_path][3]]
    # List of files that have local modification but haven't been added
    not_in_commit_list = [file_path for file_path in index_dict.keys()
                          if
                          index_dict[file_path][1] != index_dict[file_path][2]]
    # List of untracked files.
    untracked_list = [file_path for file_path in list_files
                      if file_path not in index_dict.keys()]
    return in_commit_list, not_in_commit_list, untracked_list


def list_all_in(dir_path, parent_dir, list_files=[]):
    """
    Recursively add a folder and all its child to the list of files.

    Input:
        - dir_path: the path of the current directory
        - parent_dir: the path of the lgit repository
        - list_files: The list that will be returned
    """
    # Iterate through the names of files inside the current directory
    for file in listdir(dir_path):
        # Create the relative path from lgit repository to the directory entry
        if dir_path == parent_dir:
            rel_path_from_repository = relpath(file, parent_dir)
        else:
            rel_path_from_repository = relpath(join(dir_path, file),
                                               parent_dir)
        # If it's a file, add it to the returned file list, otherwise,
        # apply this function on that folder if it's not the .lgit folder.
        if isfile(join(parent_dir, rel_path_from_repository)):
            list_files.append(rel_path_from_repository)
        elif not rel_path_from_repository.startswith(".lgit"):
            list_all_in(join(dir_path, file), parent_dir, list_files)
    return list_files


def apply_change_on_index(index_dict, parent_dir):
    """
    Update the current index file with the local changes

    Input:
        - index_dict: the dictionary contains all the infos inside the index
        file.
        - parent_dir: the path of the lgit repository
    """
    try:
        descriptor = os.open(join(parent_dir, ".lgit/index"),
                             os.O_RDWR | os.O_CREAT)
    except PermissionError:
        pathspec_error("%s/.lgit/index" % parent_dir)
        return
    for file_path, infos in index_dict.items():
        rel_path_from_repository = "%s/%s" % (parent_dir, file_path)
        try:
            file_sha1_hash = read_and_hash(rel_path_from_repository, False)
            mtime = convert_mtime_to_formatted_string(rel_path_from_repository)
            lseek(descriptor, infos[5], 0)
            update_file_index(descriptor, " ".join([mtime, file_sha1_hash]), 0)
        except FileNotFoundError:
            pass


def print_change_in_commit(commit_list):
    """
    Print changes that has been committed

    Input:
        - commit_list: list of changes that has been commited, returned by
        get_status_lst function
    """
    if not commit_list:
        return
    commit_list.sort()
    print("""
Changes to be committed:
  (use "./lgit.py reset HEAD ..." to unstage)
          """)
    for file in commit_list:
        print('     modified:', file)


def print_change_not_in_commit(non_commit_list):
    """
    Print changes that hasn't been committed

    Input:
        - non_commit_list: list of changes that hasn't been committed, returned
        by get_status_lst function
    """
    if not non_commit_list:
        return
    non_commit_list.sort()
    print(
        """
Changes not staged for commit:
  (use "./lgit.py add ..." to update what will be committed)
  (use "./lgit.py checkout -- ...  to discard changes in working directory)
        """)
    for file in non_commit_list:
        print('     modified:', file)


def print_untracked_files(untracked_list):
    """
    Print untracked files

    Input:
        - untracked_files: list of untracked files returned by
        check_untracked_files function
    """
    # If there is no untracked file, return
    if not untracked_list:
        return
    untracked_list.sort()
    print("""
Untracked files:
  (use "./lgit.py add <file>..." to include in what will be committed)
         """)
    for file in untracked_list:
        print("    ", file)
    print()


def show_status_lgit(args, parent_dir):
    """
    Show status of lgit

    Input:
        - args: The arguments parsed by the parser
        - parent_dir: the path of the lgit repository
    """
    # Get all the files from the current directory
    list_files = list_all_in(getcwd(), parent_dir)
    # Read the content of the index file
    index_dict = get_index_dictionary(parent_dir)
    # Update the index file with the current change of all tracked files.
    apply_change_on_index(index_dict, parent_dir)
    # Get the new content
    index_dict = get_index_dictionary(parent_dir)
    # Start printing
    branch = 'master'
    # branch = get_current_branch(parent_dir)
    print('On branch', branch)
    # If there is no commit, print the appropriate message
    if not has_any_commit(parent_dir):
        print('\nNo commits yet')
    # Get the changes to be commited, changes not stage for commit and
    # untracked file lists.
    commit_list, non_commit_list, untracked_list = get_status_lst(list_files,
                                                                  index_dict)
    # Print each of those list
    print_change_in_commit(commit_list)
    print_change_not_in_commit(non_commit_list)
    print_untracked_files(untracked_list)
    if not commit_list and untracked_list:
        print('nothing added to commit but untracked files present ', end='')
        print('(use "./lgit.py add" to track)')
