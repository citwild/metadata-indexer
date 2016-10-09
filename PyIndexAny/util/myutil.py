__author__ = 'Wei Wang'

import os


def path_level(path):
    path_parts = path.split(os.sep)
    return len(path_parts) - 1   # -1 for not count empty entry


def rel_level(root, full):
    return path_level(full) - path_level(root)


def is_hidden(path):
    base = os.path.basename(path)
    if base.startswith("."):
        return True
    return False


def contain_hidden_dir(path):
    path_parts = path.split(os.sep)
    for path in path_parts:
        if is_hidden(path):
            return True
    return False


def match_type(path, types):
    ext = os.path.splitext(path)[1]
    for t in types:
        with_dot = "." + t
        if with_dot.lower() == ext.lower():
            return True
    return False