#!/usr/bin/env python3


def pathspec_error(file_path):
    """
    Print an error message when a file doesn't exist or did not match
    certain conditions.

    Input:
        - file_path: The file path that is causing the error
    """
    print("fatal: pathspec '%s' did not match any files" % file_path)
    return


def add_object_permision_error():
    """
    Print an error message when you don't have permission to write on certain
    folder of lgit repository
    """
    print("Failed to add an object to lgit repository")
    return


def local_modification_error(file_path):
    """
    Print an error message when trying to remove a file with local modification

    Input:
        - file_path: The file path that is causing the error
    """
    print("error: the following file has local modifications:\n    %s"
          % file_path)
    return


def changes_stage_in_index_error(file_path):
    """
    Print an error message when trying to remove a file that has been added but
    hasn't been commmited

    Input:
        - file_path: The file path that is causing the error
    """
    print("error: the following file has changes staged in the index:\n    %s"
          % file_path)
    return
