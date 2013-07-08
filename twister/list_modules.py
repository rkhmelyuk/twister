# -*- coding: utf8 -*-

from twister import module, BUILTIN_MODULE, log

def add_arguments(parser):
    pass

def get_description():
    return "List all available modules. Use list-commands to show commands from specified module."

def get_short_description():
    return "show list of modules"

def validate(validator):
    pass

def execute(context):
    modules = module.list_modules()
    modules.remove(BUILTIN_MODULE)
    log.title("Found %d module(s)" % len(modules))
    for module_name in sorted(modules):
        log.write(" " * 4 + module_name)

    return True