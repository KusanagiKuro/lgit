#!/usr/bin/env python3
import os
from os import path, O_RDWR, O_CREAT, O_WRONLY
from index_related_funcs import *
from datetime import datetime


def none_commit(index_dict):
    no_commit = True
    count = 0
    for index in index_dict:
        if ' ' not in index[3]:
            no_commit = False
            break
    return no_commit


def changes_to_be_commit(index_dict):
    changed_file_list_cm = []
    for index in index_dict:
        if index_dict[index][2] != index_dict[index][3]:
            changed_file_list_cm.append(index)
    return changed_file_list_cm


def changes_not_staged_for_commit(index_dict):
    changed_file_list_not_cm = []
    for index in index_dict:
        if index_dict[index][2] != index_dict[index][1]:
            changed_file_list_not_cm.append(index)
    return changed_file_list_not_cm


def list_all_in(path, og_cwd, list_files=[]):
    for file in os.listdir(path):
        if path == og_cwd:
            list_files.append(file)
        else:
            list_files.append(path + '/' + file)
    for folder in list_files:
        list_all_in(path, og_cwd, list_files=[])
        if os.path.isdir(folder):
            if folder == '.lgit':
                list_files.remove(folder)
            else:
                list_files.remove(folder)
                list_all_in(folder, og_cwd, list_files)
    return list_files


def check_untracked_files(list_files, index_dict):
    untracked_files = []
    tracked_files = []
    for index in index_dict:
        tracked_files.append(index_dict[index][4])
    for file in list_files:
        if file not in tracked_files:
            untracked_files.append(file)
    return untracked_files


def show_status_lgit(args, parent_dir):
    og_cwd = os.getcwd()
    list_files = list_all_in(parent_dir, og_cwd)
    index_dict = get_index_dictionary(parent_dir)
    print('On branch master')
    if none_commit(index_dict):
        print('\nNo commits yet\n')
    if changes_to_be_commit(index_dict):
        print('Changes to be committed:')
        print('  (use "./lgit.py reset HEAD ..." to unstage)\n')
        for file in changed_file_list_cm:
            print('     modified:', file)
        print('\n')
    if changes_not_staged_for_commit(index_dict):
        print('Changes not staged for commit:')
        print('  (use "./lgit.py add ..." to update what will be committed)')
        print('  (use "./lgit.py checkout -- ..."', end='')
        print(' to discard changes in working directory)\n')
        for file in changed_file_list_not_cm:
            print('     modified:', file)
        print('\n')
    if check_untracked_files(list_files, index_dict):
        print('Untracked files:')
        print('  (use "./lgit.py add <file>..." to ', end='')
        print('include in what will be committed)\n')
        for file in untracked_files:
            print('     '+file)
        print('\n')
        print('nothing added to commit but untracked files present ', end='')
        print('(use "./lgit.py add" to track)')
