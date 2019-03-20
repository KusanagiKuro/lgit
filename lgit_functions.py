#!/usr/bin/env python3
import os
from utility import try_and_pass_function
from index_related_funcs import *
from os import mkdir, environ


def init_lgit():
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
