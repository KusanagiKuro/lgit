#!/usr/bin/env python3


def commit_lgit(args, parent_dir):
    config_file_path = path.join(parent_dir, ".lgit/config")
    try:
        config_file = open(config_file_path, "r+")
    except PermissionDenied:
        print("Unable to access", config_file_path)
        return
    pass
