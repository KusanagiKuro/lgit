#!/usr/bin/env python3
import os
from os import path, O_RDWR, O_CREAT, O_WRONLY, listdir
from os.path import join, isdir
from index_related_funcs import *
from datetime import datetime
from utility import read_and_hash, convert_mtime_to_formatted_string


def has_any_commit(parent_dir):
    return listdir(join(parent_dir, ".lgit/snapshots"))


def get_status_lst(list_files, index_dict):
    in_commit_list = []
    not_in_commit_list = []
    untracked_list = []
    for file_path in index_dict.keys():
        if index_dict[file_path][2] == index_dict[file_path][3]:
            in_commit_list.append(file_path)
        else:
            not_in_commit_list.append(file_path)
    for file_path in list_files:
        if (file_path not in index_dict.keys() or
                index_dict[file_path][1] != index_dict[file_path][2]):
            untracked_list.append(file_path)
    return in_commit_list, not_in_commit_list, untracked_list


def list_all_in(dir_path, parent_dir, list_files=[]):
    for file in listdir(dir_path):
        if dir_path == parent_dir:
            list_files.append(file)
        else:
            list_files.append(dir_path + '/' + file)
    for folder in list_files:
        if isdir(folder):
            list_files.remove(folder)
            if folder != '.lgit':
                list_all_in(folder, parent_dir, list_files)
    return list_files


def apply_change_on_index(index_dict, parent_dir):
    try:
        descriptor = os.open("%s/.lgit/index" % parent_dir,
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
    list_files = list_all_in(parent_dir, parent_dir)
    index_dict = get_index_dictionary(parent_dir)
    apply_change_on_index(index_dict, parent_dir)
    index_dict = get_index_dictionary(parent_dir)
    print('On branch master')
    if not has_any_commit(parent_dir):
        print('\nNo commits yet')
    commit_list, non_commit_list, untracked_list = get_status_lst(list_files,
                                                                  index_dict)
    print_change_in_commit(commit_list)
    print_change_not_in_commit(non_commit_list)
    print_untracked_files(untracked_list)
    if not commit_list and untracked_list:
        print('nothing added to commit but untracked files present ', end='')
        print('(use "./lgit.py add" to track)')
