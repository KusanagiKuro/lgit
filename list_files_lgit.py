#!/usr/bin/env python3
from index_related_funcs import get_index_dictionary
from os import getcwd
from os.path import dirname, isfile, relpath


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
                          if getcwd()
                          in dirname("%s/%s" % (parent_dir, infos[4]))
                          and isfile("%s/%s" % (parent_dir, infos[4]))]
    # Sort then print their path
    tracking_path_list.sort()
    for file_path in tracking_path_list:
        print(relpath(file_path))
