# -*- coding: utf8 -*-

from twister import log
from twister.alias import load_aliases, ALIAS

def add_arguments(parser):
    pass

def get_description():
    return "List all available aliases. Aliases are stored in file '%s' in the Twister directory. Refer to this file to edit aliases." % ALIAS

def get_short_description():
    return "show list of aliases"

def validate(validator):
    pass

def execute(context):
    aliases = load_aliases()
    log.title("Found %d alias(es)" % len(aliases))
    for alias, alias_to in sorted(aliases.items()):
        log.write(" " * 4 + ("%-20s " + log.GRAY + "%s" + log.END) % (alias, alias_to))

    return True