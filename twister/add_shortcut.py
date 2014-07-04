# -*- coding: utf8 -*-

import os
from subprocess import CalledProcessError
from twister import commands, get_twister_directory

def add_arguments(parser):
    parser.add_argument("--dest", help="destination directory, must exist; default is /usr/local/bin", default="/usr/local/bin")
    parser.add_argument("--name", help="name for the command, usually the name of the project; default is twister", default="twister")

def get_description():
    return "Add shortcut to the twister, that allows to run twister from any directory. By default adds shortcut to the" \
           " /usr/local/bin directory, but can be added to other directory, specified by --dest argument. Also default name" \
           " is 'twister', but could and should be changed to the project name, as multiple different twister installation" \
           " would be used in parallel."

def get_short_description():
    return "add twister shortcut"

def validate(validator):
    pass

def execute(context):
    try:
        twister_runner = os.path.join(get_twister_directory(), "twister.sh")
        commands.execute("ln -s %s %s" % (twister_runner, os.path.join(context.args.dest, context.args.name)),
                         output=context.args.verbose,
                         error_text="Failed to add shortcut")
        commands.execute("chmod 744 %s" % twister_runner)
        return True
    except CalledProcessError:
        return False
