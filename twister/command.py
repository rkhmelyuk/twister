# -*- coding: utf8 -*-
import argparse
import os
import time
from twister import get_twister_directory, BUILTIN_MODULE, log

PROJECT_PATH_ARG = "--use-project-path"
TWISTED_PATH_ARG = "--use-twisted-path"

class Command:
    def __init__(self, module, module_name, command_name, command_module_path):
        self.module = module
        self.module_name = module_name
        self.command_name = command_name
        self.command_module_path = command_module_path

    def __str__(self):
        if self.module_name == BUILTIN_MODULE:
            return self.command_name
        return "%s %s" % (self.module_name, self.command_name)

    def __repr__(self):
        return "Command(%s,%s)" % (self.module_name, self.command_name)

    def validate(self):
        if self.module is None:
            print "Not found module %s" % self.command_module_path
            return False

        # -----------------------------------------------------------------
        # TODO - validate that command has all required functions
        # -----------------------------------------------------------------

        return True

    def execute(self, context, show_exec_time=True):
        validator = Validator(context)
        self.module.validate(validator)
        if not validator.is_valid():
            if validator.is_show_usage():
                self.show_help()
            return False

        begin = time.time()
        try:
            return self.module.execute(context)
        finally:
            if show_exec_time:
                print(log.GRAY + ("Done in %0.3f seconds" % (time.time() - begin)) + log.END)

    def get_arg_parser(self):
        import argparse
        import os.path
        import sys

        prog = os.path.basename(sys.argv[0])
        if self.module_name == 'twister':
            prog_name = "%s %s" % (prog, self.command_name)
        else:
            prog_name = "%s %s %s" % (prog, self.module_name, self.command_name)

        parser = argparse.ArgumentParser(add_help=False, prog=prog_name, description=self.module.get_description())
        parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
        self.module.add_arguments(parser)
        parser.add_argument("--verbose", help="show more information than usual including output of executed commands", action="store_true")

        return parser

    def show_help(self):
        self.get_arg_parser().print_help()

    def get_help(self):
        return self.get_arg_parser().format_help()

    def get_short_description(self):
        return self.module.get_short_description()

def build_command_context(command, args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(TWISTED_PATH_ARG)
    parser.add_argument(PROJECT_PATH_ARG)
    parser.add_argument("--verbose", action="store_true")

    parsed_args, unknown = parser.parse_known_args()

    # use use-project-path and use-twisted-path to specify value, but remove from parsed args
    project_path = parsed_args.use_project_path
    twisted_path = parsed_args.use_twisted_path

    twister_directory = get_twister_directory()
    if not project_path:
        # use the $PROJECT_PATH env var
        project_path = os.environ.get('PROJECT_PATH')
    if not project_path:
        # the default one is parent directory
        project_path = os.path.dirname(twister_directory)

    if not twisted_path:
        # use the $TWISTED_PATH env var
        twisted_path = os.environ.get("TWISTED_PATH")
    if not twisted_path:
        # the default one is twisted directory in parent directory
        twisted_path = os.path.join(os.path.dirname(twister_directory), "twisted")

    if not os.path.exists(twisted_path):
        os.mkdir(twisted_path)
        print "Created twisted directory: %s" % twisted_path
    elif not os.path.isdir(twisted_path):
        print "%s is not directory" % twisted_path
        exit(-1)

    if parsed_args.verbose:
        log.info("Detected command: %s" % str(command))
        log.info("Use project at %s" % project_path)
        log.info("Use twisted at %s" % twisted_path)

    command_args = get_command_arguments(args)
    parsed_args = command.get_arg_parser().parse_args(command_args)

    return Context(command=command, twisted_path=twisted_path, project_path=project_path, args=parsed_args)

def get_command_arguments(args):
    """ filter out arguments not relevant to command """
    command_args = []
    skip_next_arg = False
    for arg in args:
        if skip_next_arg:
            skip_next_arg = False
            continue

        if arg.startswith(TWISTED_PATH_ARG):
            skip_next_arg = arg == TWISTED_PATH_ARG
        elif arg.startswith(PROJECT_PATH_ARG):
            skip_next_arg = arg == PROJECT_PATH_ARG
        else:
            command_args.append(arg)

    return command_args

class Context:
    def __init__(self, command, twisted_path, project_path, args):
        self.args = args
        self.command = command
        self.twisted_path = twisted_path
        self.project_path = project_path

    def __str__(self):
        return "Context[%s,%s,%s]" % (self.twisted_path, self.project_path, self.args)

    def __repr__(self):
        return "Context[%s,%s,%s]" % (self.twisted_path, self.project_path, self.args)

class Validator:
    def __init__(self, context):
        self.context = context
        self.valid = True
        self.show_usage = False

    def project_path_required(self):
        """ Check if project path is specified and it exists """

        if not self.valid: return

        self.valid = False
        if not self.context.project_path:
            log.error("project path is not specified")
            return
        if not os.path.exists(self.context.project_path):
            log.error("project path %s is not found" % self.context.project_path)
            return

        self.valid = True

    def no_args_conflicts(self, *args):
        """ Check there is not conflicts between arguments """
        if not self.valid: return

        num = 0
        found_args = []
        for arg in args:
            attr = getattr(self.context.args, arg, None)
            if attr:
                num += 1
                found_args.append(arg)

        if num > 1:
            self.valid = False
            self.show_usage = True
            log.error("Found conflict between arguments [%s], which can't be used together.\n" % ", ".join(found_args))

    def arg_required(self, arg_name):
        """ Check that required argument is specified """
        if not self.valid: return

        attr = getattr(self.context.args, arg_name, None)
        if not attr:
            self.valid = False
            self.show_usage = True
            log.error("Argument %s is not specified, but required\n" % arg_name)

    def any_arg_required(self, *args):
        if not self.valid: return

        num = 0
        for arg in args:
            attr = getattr(self.context.args, arg, None)
            if attr:
                num += 1

        if num == 0:
            self.valid = False
            self.show_usage = True
            log.error("At least one of [%s] arguments is required.\n" % ", ".join(args))

    def not_empty(self, arg_name):
        arg_value = getattr(self.context.args, arg_name, None)
        if arg_value is None:
            return

        if len(arg_value) == 0:
            self.valid = False
            log.error("No value specified for [%s]" % arg_name)


    def is_valid(self):
        return self.valid

    def is_show_usage(self):
        return self.show_usage