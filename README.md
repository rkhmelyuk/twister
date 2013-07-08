Twister
=======

Twister is a tool to group and run other tools, usually project specific tools. 
It already has some built-in commands that allows to discover other commands. And it's easy to extend twister with
new modules and commands.

Module represent some sub-set of commands, like there could be a module to work with databases, some development tools etc.
Twister gives some unique simple way to organize how you work with CLI tools within project.

## Getting Started

### Shortcut
First, add shortcut to the twister script, to simplify work with it. It's possible to add shortcut using twister:

    cd twister
    python twister.py add-shortcut                 # add shortcut /usr/local/bin
    python twister.py add-shortcut --dest ~/bin    # add shortcut to ~/bin/

Now it's possible to use `twister` from any directory.

Now that we have twister downloaded and shortcut available, we can start using it. Enter next command to see twister help and
options available:

    twister

### twister usage

You'll see that twister is command oriented, and that each command belongs to specified module. Module name is optional,
and it can be skipped when run built-in commands, for example:

    twister list-commands           # built-in command
    twister dev clean               # command clean from module build

Command names can be duplicate over the modules, but should stay unique in the same module.

In it's work, twister needs to know 3 paths:

 - project path: the path to the directory where project is located
 - twisted path: the path to the twister working directory
 - twister path: the path to the twister directory, where twister.py and other scripts are located.

While twister path is get by twister.py location, project path and twisted path may be different. By default, project path
is assumed to be the parent directory of twister directory, and twisted path is expanded to the twisted directory in the project path.
However, it's possible to override project and twisted paths, using `--use-project-path` and `--use-twisted-path` arguments.

### exploring twister

Built-in commands are helpful to explore the twister available modules and commands, get help information for each module. They are
both a great starting point to using twister, as well as useful commands for everyday use.

#### list-modules

    twister list-modules

Shows the list of available modules.

#### list-commands

    twister list-commands

Shows the list of all available commands grouped by modules. It's also possible to get the list of commands in some specific module,
using next command:

    twister list-commands --module dev

or it's alias

    twister dev list-commands

If you need to get list of built-in commands, use `--built-in` argument:

    twister list-commands --built-in

#### help

    twister help {command}

Shows help information for specified command. If found multiple command by specified name, than twister will show list of such commands
and ask you to choose only one by adding `--module [module]` argument.

    twister help clean --module dev

Or the same, but in simpler way:

    twister dev help clean

To get information about `help` command, just run one of next commands:

    twister help help
    twister help --help

All commands supports `--help` argument, that will show help information for specified command

    twister dev clean --help

which is the same as `twister dev help clean`

#### find-command

    twister find-command {pattern}

Finds all commands that contain specified pattern and prints them. This command uses command names, command module name and command short
description to find the commands. The commands are also listed in the order of match: first shows matched by name, then by module and
then by description.

Also possible to search for command within some module using command:

    twister find-command clean --module dev

or it's alias:

    twister dev find-command clean

Thus, using `list-commands` and `find-command` it's possible to get the command you need, and `help` will show help
and usage information about it.

## Hints

### Shortcut

Twister contains `twister.sh` script, that is responsible to start a twister application. This script
is written in the way it can be run from any directory, or it's possible to create a symbolic link to
this shell script and run it. This is actually a recommended way: create a symlink and put it to your
`~/bin` directory (make sure that `bin/` directory is in `$PATH`):

    ln -s {project_path}/twister/twister.sh ~/bin/twister

Now it's possible to run commands from any directory, and it will be able to resolve twister and project
directory, and execute command for them:

    cd /usr/local    		    # go to some directory
    twister list-commands		# still working

It's possible to add shortcut with built-in command `add-shortcut`:

    python twister.py add-shortcut                 # add shortcut /usr/local/bin
    python twister.py add-shortcut --dest ~/bin    # add shortcut to ~/bin/


### Built-in commands within module

Some built-in commands like `list-commands`, `help` or `find-command` can narrow it's work for specified module using `--module` argument,
for example:

    twister find-command clean --module dev
    twister help clean --module dev
    twister list-commands --module db

Although these commands belong to the built-in module (ie `twister`), it's possible to use them within some module:

    twister dev find-command clean
    twister db list-commands
    twister runtime find-command list

How this works? Well, when Twister finds that command is not in module, it checks if such command exists in the built-in module.
And if it's true, then it uses that command and pass module name as argument via `--module`. No checks whether this command
can accept `--module` argument are done. This means, that this won't work for all built-in commands. For example, command
`list-modules` doesn't accept `--module` argument. Means, you'll see error if run something like that:

    twister dev list-modules

So, simply put, the command:

    twister dev find-command clean

is converted to:

    twister find-command --module dev clean

and executed.


### Aliases

There are also a few commands that are used to often, and it might be time consuming entering them again and again.
Replacing thus commands with shorter command can be very convenient. That's why twister has aliases.

Twister allows to replace command with arguments with some alias. Aliases are configure by editing file `alias` in
twister directory. It's also possible to get the list of aliases using command:

    twister list-aliases

or its alias:

    twister aliases

It's possible to specify arguments for aliases, thus one can create alias `run-some-app` => `runtime run some-app`.

There is a list of predefined aliases:

 - `aliases` => `list-aliases`
 - `commands` => `list-commands`
 - `modules` => `list-modules`
