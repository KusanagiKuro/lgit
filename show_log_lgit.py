#!/usr/bin/env python3
import os
from datetime import datetime
from os import path


def show_log_lgit(args, parent_dir):
    """
    Show the history of commits, from newest to oldest

    Input:
        - args: the arguments that were parsed by the parser
        - parent_dir: the directory that contains the lgit repository
    """
    def get_mtime(dir_entry):
        """
        Get the modification time of a directory entry

        Input:
            - dir_entry: A DirEntry object of the commit object
        """
        return dir_entry.stat().st_mtime
    # Get the list of commit files
    dir_entry_list = [dir_entry for dir_entry
                      in os.scandir(parent_dir + "/.lgit/commits")
                      if path.isfile(dir_entry.path)]
    # Sort these files by their modification time
    dir_entry_list.sort(key=get_mtime)
    # Print the log for each commit file
    while dir_entry_list:
        dir_entry = dir_entry_list.pop()
        print_log(dir_entry)


def print_log(dir_entry):
    """
    Print the log from a commit directory entry

    Input:
        - dir_entry: A DirEntry object of the commit object
    """
    # Read and transform all the needed infos
    try:
        commit_file = open(dir_entry.path, "r")
        content = commit_file.readlines()
        # Get author name
        author = content[0].strip()
        # Get the time from commit file and reformat it
        datetime_text = " ".join([content[1][:4],
                                  content[1][4:6],
                                  content[1][6:8],
                                  content[1][8:10],
                                  content[1][10:12],
                                  content[1][12:-1]])
        # Convert it to human-readable date and time
        date = datetime.strptime(datetime_text, "%Y %m %d %H %M %S").ctime()
    except PermissionError:
        return
    # Print all the infos
    print("commit", dir_entry.name)
    print("Author:", author)
    print("Date:", date, end="\n\n")
    print("   " + content[3])
    print()
