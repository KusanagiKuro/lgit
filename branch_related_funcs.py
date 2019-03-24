#!/usr/bin/env python3


def get_current_branch(parent_dir):
    """
    Get the name of the current branch

    Input:
        - parent_dir: the path to the lgit repository
    """
    current_branch = None
    # Open the HEAD file and read the branch name
    try:
        with open(join(parent_dir, ".lgit/HEAD"), "w+") as head_file:
            current_branch = head_file.read().strip().split("/")[-1]
    except (PermissionError, FileNotFoundError, IsADirectoryError):
        print("Reading branch name failed")
    return current_branch


def update_current_branch(current_branch, commit_name):
    """
    Update the commit that the current branch is pointing at

    Input:
        - current_branch: the name of the current branch
        - commit_name: the name of the new commit
    """
    try:
        with open(parent_dir + ".lgit/refs/heads/" + current_branch,
                  "w+") as branch:
            branch.write(commit_name)
    except (PermissionError, FileNotFoundError, IsADirectoryError):
        print("Update branch failed")


def get_last_commit(current_branch):
    """
    Get the last commit's file name from the current branch head file.

    Input:
        - current_branch: the name of the current branch
    """
    try:
        with open(parent_dir + ".lgit/refs/heads/" + current_branch) as branch:
            return branch.read().strip()
    except (PermissionError, FileNotFoundError, IsADirectoryError):
        print("Getting last commit failed")
        return None
