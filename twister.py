# -*- coding: utf8 -*-
import re
import sys
from twister import log
from twister.alias import load_aliases
from twister.command import build_command_context, PROJECT_PATH_ARG, TWISTED_PATH_ARG
from twister.module import load_commands_from_module, load_builtin, list_modules

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(-1)

    args, command_name, module_name = get_twister_args()

    builtin_commands = load_builtin()

    if module_name is None:
        if not command_name:
            log.error("Missing command name. See usage below:")
            print_help()
            sys.exit(-1)
        if command_name not in builtin_commands.keys():
            log.error("Unknown command: %s" % command_name)
            log.help(("Run " + log.command("find-command %s") + " to find command.") % command_name)
            sys.exit(-1)
    elif module_name in builtin_commands.keys():
        command_name = module_name
        module_name = None
        args = sys.argv[2:]

    command = None
    if module_name is None:
        command = builtin_commands[command_name]
    else:
        if module_name not in list_modules():
            log.error("Unknown module %s." % module_name)
            log.help("Run " + log.command("list-modules") + " to get list of available modules")
            sys.exit(-1)
        commands = load_commands_from_module(module_name)
        if command_name not in commands.keys():
            if command_name in builtin_commands.keys():
                # interesting hook for built-in commands to allow them use within specified module
                command = builtin_commands[command_name]
                args.append("--module")
                args.append(module_name)
            else:
                # command not found in module
                log.error("Unknown command %s in module %s." % (command_name, module_name))
                log.help(("Run " + log.command("%(module)s list-commands") +
                          " to get list of available commands in module %(module)s.") % dict(module=module_name))
                log.help(("Run " + log.command("find-command %s") + " to find command.") % command_name)
                sys.exit(-1)

        # in case if command already found in built-ins
        command = command or commands[command_name]

    if not command.validate():
        sys.exit(-1)

    context = build_command_context(command, args)

    if not command.execute(context):
        sys.exit(-1)


def get_twister_args(args=sys.argv[1:]):
    module_name = None
    command_name = None
    command_args = []

    # read module and command
    if len(args) == 1:
        command_name = args[0]
        command_args = []
    elif len(args) >= 2:
        module_name = args[0]
        command_name = args[1]
        command_args = args[2:]

    # -- handle the case when we have only parameters or command + parameter
    if module_name and module_name.startswith("--"):
        module_name = None
    if command_name and command_name.startswith("--"):
        command_name = module_name
        module_name = None
        command_args = args[1:]

    # -- if module name is incorrect, this might be a command..
    if module_name and module_name not in list_modules():
        command_name = module_name
        command_args = args[1:]
        module_name = None

    # -- handle the aliases
    if not module_name:
        aliases = load_aliases()
        if command_name in aliases.keys():
            log.info("Using alias '%s' => '%s'" % (command_name, aliases[command_name]))
            alias_parts = re.split("\s+", aliases[command_name])
            alias_args, command_name, module_name = get_twister_args(alias_parts)
            # sum up alias args and command args
            command_args = alias_args + command_args

    return command_args, command_name, module_name

def print_help():
    print """usage: twister [module] command [%(pp)s] [%(tp)s] [args] [--verbose]

Run %(list_command)s to show a list of all available commands
and %(help_command)s to show help information for specified command.

arguments:
  module              module that contains the command, if not specified then
                      execute built-in command
  command             name of the command that has to be executed
  args                command arguments
  %(pp)s  specify the project directory
                      by default it is parent directory
  %(tp)s  specify path to the twisted directory, by default it is '../twisted'
  --verbose           show more information than usual including output of
                      executed commands""" % \
          dict(pp=PROJECT_PATH_ARG, tp=TWISTED_PATH_ARG,
               list_command=log.command("list-commands"),
               help_command=log.command("help <command>"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by CTRL+C")