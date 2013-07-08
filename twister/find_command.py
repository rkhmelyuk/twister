# -*- coding: utf8 -*-

from twister import module, log

def add_arguments(parser):
    parser.add_argument("command", help="name of command to find")
    parser.add_argument("--module", help="find command within specified module")

def get_description():
    return "Finds matched by name commands. It will print module commands if searched command is same as module name. It also " \
           "searched in command short description, of searched command length is 3 and more characters. Outputs list of matched " \
           "commands starting with best matched on top."

def get_short_description():
    return "find commands by name"

def validate(validator):
    pass

def execute(context):
    command_name = context.args.command
    module_name = context.args.module

    best_matched_commands = []
    matched_module_commands = []
    matched_description_commands = []

    modules = module.list_modules()
    if module_name:
        if module_name not in modules:
            log.error("Unknown module %s" % module_name)
            return False
        # module name is specified, find commands in this module only
        modules = [module_name]


    for module_name in modules:
        module_commands = module.load_commands_from_module(module_name)
        for module_command_name, command in module_commands.items():
            if command_name in module_command_name:
                best_matched_commands.append(command)
            elif module_name == command_name:
                # include all module_commands if module name is
                # same as searched command
                matched_module_commands.append(command)
            elif len(command_name) >= 3 and (command_name in command.get_short_description() or command_name in command.get_help()):
                # include command if searched command is mentioned
                # in the description
                matched_description_commands.append(command)

    matched_commands = best_matched_commands + matched_module_commands + matched_description_commands
    if not matched_commands:
        print "No commands found"
        return False

    print ("[ Found %d commands ]" % len(matched_commands)).ljust(80, "-")
    for command in sorted(best_matched_commands):
        show_command_info(command)
    for command in sorted(matched_module_commands):
        show_command_info(command)
    for command in sorted(matched_description_commands):
        show_command_info(command)

    return True

def show_command_info(command):
    print " " * 4 + ("%-25s" + log.GRAY + "%s" + log.END) % (str(command), command.get_short_description())
