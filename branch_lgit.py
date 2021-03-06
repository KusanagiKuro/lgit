#!/usr/bin/env python3
from os import getcwd, listdir, path, remove
from utility import *
from show_status_lgit import has_any_commit
from branch_related_funcs import *


def branch_lgit(args, parent_dir):
    commits_path = parent_dir+'/.lgit/commits'
    if listdir(commits_path):
        with open(parent_dir+'/.lgit/refs/heads/master', 'w+') as file:
            file.write(read_and_hash(parent_dir+'/.lgit/refs/heads/master')[0])
        if not args.name:
            list_all_branch(parent_dir)
        else:
            if not has_any_commit(parent_dir):
                return
            if check_exist_branch(args.name, parent_dir):
                print("fatal: A branch named '"+args.name+" already exists.")
            else:
                create_new_branch(args.name, parent_dir)
    else:
        if path.exists(parent_dir+'/.lgit/refs/heads/master'):
            remove(parent_dir+'/.lgit/refs/heads/master')
        print('fatal: Not a valid object name: \'master\'.')


def list_all_branch(parent_dir):
    cur_branch = find_cur_branch(parent_dir)
    list_branchs = listdir(parent_dir+'/.lgit/refs/heads')
    list_branchs.sort()
    for branch in list_branchs:
        print("*" if branch == cur_branch else " ", branch)


def find_cur_branch(parent_dir):
    cur_branch = None
    with open(parent_dir+'/.lgit/HEAD', 'r') as file:
        head_line = file.read().strip()
        cur_branch = head_line.split("/")[-1]
    return cur_branch


def check_exist_branch(branch, parent_dir):
    return path.exists(parent_dir+'/.lgit/refs/heads/'+branch)


def create_new_branch(branch, parent_dir):
    branch_path = parent_dir+'/.lgit/refs/heads/'+branch
    with open(branch_path, 'w+') as file:
        # Get the list of commit files
        dir_entry_list = [dir_entry for dir_entry
                          in scandir(join(parent_dir, ".lgit/commits"))
                          if isfile(dir_entry.path)]
        # Sort these files by their modification time
        dir_entry_list.sort(key=get_mtime)
        file.write(dir_entry_list[-1].name)
