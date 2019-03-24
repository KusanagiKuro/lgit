#!/usr/bin/env python3
import os
from os import path, O_RDWR, O_CREAT, O_WRONLY
from index_related_funcs import *
from datetime import datetime


def commit_lgit(args, parent_dir):
    """
    Commit all changes

    Input:
        - args: The arguments that were parsed by the parser
        - parent_dir: the path to the lgit repository
    """
    # The path to the config file
    config_file_path = path.join(parent_dir, ".lgit/config")
    try:
        config_file = open(config_file_path, "r+")
    except PermissionError:
        print("Unable to access", config_file_path)
        return
    # Read the config file to get the author name
    content = config_file.readlines()
    if not content:
        # If it is empty, the commit shouldn't happen.
        return
    author = content[0].rstrip()
    config_file.close()
    # Read the index file
    index_dict = get_index_dictionary(parent_dir)
    if not index_dict:
        # If it is empty, there's nothing to commit, return
        return
    # Update the index file
    index_file_path = path.join(parent_dir, ".lgit/index")
    descriptor = os.open(index_file_path, O_RDWR)
    # Create the list that will contains the content would be written on the
    # snapshot object
    snapshot_content = []
    for file_path, infos in index_dict.items():
        # If a file has different SHA1 code in add field and commit field
        # update it
        if infos[2] != infos[3]:
            lseek(descriptor, infos[5], 0)
            update_file_index(descriptor, infos[2], 3)
            snapshot_content.append(" ".join([infos[2], infos[4]]))
            lseek(descriptor, 0, 0)
    os.close(descriptor)
    # Create a commit and snapshot objects
    commit_name = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S.%f")
    create_snapshot_object(commit_name, snapshot_content, parent_dir)
    create_commit_object(commit_name, author, args.message, parent_dir)


def create_commit_object(commit_name, author, message, parent_dir):
    """
    Create a commit object in commit directory

    Input:
        - commit_name: the name of the object's file
        - author: the name of the author who commited tha changes
        - message: the message for the commit
        - parent_dir: the path to the lgit repository
    """
    # The path for the new commit object
    new_object_path = "%s/.lgit/commits/%s" % (parent_dir, commit_name)
    try:
        commit_file = open(new_object_path, "w+")
    except PermissionError:
        add_object_permision_error()
        return
    # The commit time
    commit_time = commit_name.split(".")[0]
    # The text that will be written on the commit object
    text = "\n".join([author, commit_time, "", message[0]])
    commit_file.write(text + "\n")
    commit_file.close()


def create_snapshot_object(commit_name, content, parent_dir):
    """
    Create the snapshot object

    Input:
        - commit_name: the name of the object's file
        - content: the content that will be written on the snapshot
        - parent_dir: the path to the lgit repository
    """
    # The path for the new snapshot object
    new_object_path = "%s/.lgit/snapshots/%s" % (parent_dir, commit_name)
    try:
        snapshot_file = open(new_object_path, "w+")
    except PermissionError:
        add_object_permision_error()
        return
    text = "\n".join(content)
    # Write the content
    snapshot_file.write(text + "\n")
    snapshot_file.close()
