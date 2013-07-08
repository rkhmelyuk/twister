# -*- coding: utf8 -*-
import os

from twister import get_twister_directory
from twister import log
from twister.command import Command
from twister.command import build_command_context

COMMANDS = "_commands.py"


def list_modules():
    """ Returns the list of all modules available """
    twister_directory = get_twister_directory()
    files = os.listdir(twister_directory)
    modules = []

    for child_file in files:
        path = os.path.join(twister_directory, child_file)
        if not os.path.isdir(path):
            continue
        commands = os.path.join(path, COMMANDS)
        if os.path.exists(commands) and os.path.isfile(commands):
            modules.append(child_file)

    return modules


def load_commands_from_module(module_name):
    """ load commands from specified module """
    twister_directory = get_twister_directory()
    module_path = os.path.join(twister_directory, module_name)
    module_commands_file_path = os.path.join(module_path, COMMANDS)
    module = load_py_module('%s_commands' % module_name, module_commands_file_path)
    commands = {}
    if module:
        for command_name, command_module_name in module.commands.items():
            command_module_path = os.path.join(module_name, command_module_name)
            command_module_path = os.path.join(twister_directory, command_module_path)

            # TODO - prefer to use module loader...
            module = load_py_module(command_name, command_module_path)
            commands[command_name] = Command(module, module_name, command_name, command_module_path)
    return commands

def load_py_module(module_name, path):
    import imp

    try:
        return imp.load_source(module_name, path)
    except IOError:
        # file is not found, log and return None
        log.error("module %s is not found" % path)
        return None

def load_builtin():
    return load_commands_from_module("twister")

def find_and_execute(parent_context, module, command, args=()):
    module_commands = load_commands_from_module(module)
    module_command = module_commands.get(command, None)
    if module_command:
        cmd_args = list(args)

        # add twisted path and project path
        cmd_args.append('--use-twisted-path')
        cmd_args.append(parent_context.twisted_path)
        cmd_args.append('--use-project-path')
        cmd_args.append(parent_context.project_path)

        # add verbose parameter if need
        verbose = getattr(parent_context.args, 'verbose', False)
        if verbose: cmd_args.append("--verbose")

        context = build_command_context(module_command, cmd_args)
        log.title("command %s %s" % (module_command, " ".join(args)))
        return module_command.execute(context, show_exec_time=False)
    else:
        log.error("Command %s %s is not found" % (module, command))

    return False