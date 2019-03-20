#!/usr/bin/env python3
import os
from os import mkdir, environ, path, O_RDONLY, O_RDWR, O_CREAT, lseek
from utility import handle_path, hash_file_content, read_index_file


def init_lgit(args):
    """
    Initialize the directories structure
    """
    # Create lgit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit")
    # Create objects directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/objects")
    # Create commit directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/commits")
    # Create snapshots directory
    try_and_pass_function(mkdir, FileExistsError, "./.lgit/snapshots")
    # Create index file
    index = open("./.lgit/index", "w")
    # Create config file, write the user name on it
    config = open("./.lgit/config", "w")
    # Write the username to the config file
    config.write(environ.get("USER"))
    index.close()
    config.close()


def commit_lgit(args, parent_dir):
    pass


def remove_lgit(args, parent_dir):
    pass


def config_lgit(args, parent_dir):
    pass


def show_status_lgit(args, parent_dir):
    pass


def list_files_lgit(args, parent_dir):
    pass


def show_log_lgit(args, parent_dir):
    pass
