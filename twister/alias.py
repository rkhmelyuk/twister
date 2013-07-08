# -*- coding: utf8 -*-

import os
from twister import get_twister_directory

ALIAS = "alias"
ALIASES = os.path.join(get_twister_directory(), ALIAS)

def load_aliases():
    """ Loads the list of available aliases from special file """
    alias_file = open(ALIASES, 'r')
    aliases = {}
    for line in alias_file.readlines():
        line = line.strip()
        if line.startswith("#") or len(line) == 0:
            # skip comments and empty lines
            continue

        # read alias
        info = line.split("=", 1)
        if len(info) == 2:
            aliases[info[0]] = info[1]

    alias_file.close()

    return aliases