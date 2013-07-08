# -*- coding: utf8 -*-

from twister import module, BUILTIN_MODULE, log

def add_arguments(parser):
    parser.add_argument("--module", help="list commands only for specified module")
    parser.add_argument("--built-in", help="list built-in commands only", action="store_true")

def get_description():
    return "List all available commands, or only commands for specified module. If neither " \
           "--module nor --built-in are specified, then shows all commands."

def get_short_description():
    return "show list of commands"

def validate(validator):
    pass


def execute(context):
    commands = {}
    if context.args.built_in:
        commands.update({BUILTIN_MODULE: module.load_builtin()})
    if context.args.module:
        module_name = context.args.module
        commands.update({module_name: module.load_commands_from_module(module_name)})
    if not context.args.built_in and not context.args.module:
        modules = module.list_modules()
        for module_name in modules:
            commands[module_name] = module.load_commands_from_module(module_name)

    builtin_commands = commands.get(BUILTIN_MODULE, [])
    if builtin_commands:
        print_module_with_commands("built-in", builtin_commands)

    for module_name, module_commands in sorted(commands.items()):
        if module_name == BUILTIN_MODULE: continue

        print_module_with_commands(module_name, module_commands)

    return True

def print_module_with_commands(module_name, module_commands):
    log.title(module_name)
    for command_name, command in sorted(module_commands.items()):
        log.write(" " * 4 + ("%-25s " + log.GRAY + "%s" + log.END) % (str(command), command.get_short_description()))
