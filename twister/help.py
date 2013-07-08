# -*- coding: utf8 -*-

from twister import BUILTIN_MODULE
from twister import log
from twister.module import list_modules, load_commands_from_module

def add_arguments(parser):
    parser.add_argument("command", help="help information for specified command")
    parser.add_argument("--module", help="show help information for command in specified module")
    parser.add_argument("--built-in", help="show help information for built-in command", action="store_true")

def get_description():
    return "show information about other commands"

def get_short_description():
    return "show help information for command"

def validate(validator):
    validator.no_args_conflicts('built_in', 'module')

def execute(context):
    # choose which module(s) to look for command
    if context.args.built_in:
        modules = [BUILTIN_MODULE]
    elif context.args.module:
        modules = [context.args.module]
    else:
        modules = list_modules()

    matched_commands = []
    for module_name in modules:
        commands = load_commands_from_module(module_name)
        found_command = commands.get(context.args.command, None)
        if found_command:
            matched_commands.append(found_command)

    if len(matched_commands) == 0:
        log.error("Command %s is not found" % context.args.command)
        return False
    elif len(matched_commands) == 1:
        matched_commands[0].show_help()
    else:
        log.title("Found multiple commands")
        log.write("Use suggested argument to show help for specified command only.")
        for command in matched_commands:
            if command.module_name == BUILTIN_MODULE:
                narrow_help = "run with --built-in"
            else:
                narrow_help = "run with --module=%s" % command.module_name
            log.write(" " * 4 + "%-25s%s" % (str(command), narrow_help))

    return True