# -*- coding: utf8 -*-

BUILTIN_MODULE = "twister"

twister_directory = None

def get_twister_directory():
    global twister_directory

    # return if already initialized
    if twister_directory: return twister_directory

    import os
    import sys

    # current directory changes all the time, so we want to cache correct
    # twister directory that we calculated on first call (before any cd)
    twister_directory = os.path.split(os.path.realpath(sys.argv[0]))[0]

    return twister_directory

# should go after get_twister_directory() as module imports get_twister_directory
from module import find_and_execute