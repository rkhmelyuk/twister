# -*- coding: utf8 -*-

import os
import shutil
import fnmatch
import subprocess

from twister import log

DEVNULL = open(os.devnull, 'wb')

def mkdir(path):
    """ Create a directory if need """
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def rmdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def remove(path):
    if os.path.exists(path):
        os.remove(path)

def cd(path):
    os.chdir(path)

def append_file(file_path, text):
    subprocess.call("echo '%s' >> %s" % (text, file_path), shell=True)

def copyfile(source, target, skip=()):
    subprocess.call("cp -f %s %s" % (source, target), shell=True)
    remove_skipped(target, skip)

def copydir(source, target, skip=()):
    subprocess.call("cp -fr %s %s" % (source, target), shell=True)
    remove_skipped(target, skip)

def remove_skipped(target, skip):
    # we copy everything, but then remove files that need to be skipped
    for each in skip:
        each_path = os.path.join(target, each)
        if os.path.isdir(each_path):
            rmdir(each_path)
        else:
            remove(each_path)

def copyfiles(source, target):
    subprocess.call("cp -fr %s/* %s" % (source, target), shell=True)

def execute(command, output=False, show_command=True, command_title=None, output_on_error=True, error_text=None, checked=True):
    """ executes the command """
    if show_command:
        if command_title:
            title = "~ " + command_title
        elif output:
            title = command
        else:
            title = command if len(command) < 70 else command[0:20] + " ... " + command[-20:]

        log.title("execute " + title)

    if not checked:
        return subprocess.call(command, shell=True, stdout=(None if output else DEVNULL), stderr=(None if output else DEVNULL))

    if output:
        try:
            return subprocess.check_call(command, shell=True, stdout=(None if output else DEVNULL), stderr=(None if output else DEVNULL))
        except subprocess.CalledProcessError as e:
            if error_text: log.error(error_text)
            raise e

    try:
        subprocess.check_output(command, shell=True)
        return 0
    except subprocess.CalledProcessError as e:
        if output_on_error: print_failed_command_output(e)
        if error_text: log.error("%s: error code %d. Run with --verbose flag to see more output" % (error_text, e.returncode))
        raise e


def execute_and_return_output(command):
    output = subprocess.check_output(command, shell=True)
    lines = output.splitlines()
    return lines[0].strip() if lines else ""

def command_exists(command, output=False):
    retcode = subprocess.call("which %s" % command, shell=True, stdout=(None if output else DEVNULL))
    return retcode == 0

def execute_background_and_return_pid(*args):
    process = subprocess.Popen(args, shell=False, stdout=DEVNULL)
    return process.pid

def print_failed_command_output(e):
    if e.output:
        log.info("Command output:")
        for line in str(e.output).splitlines():
            line_lower = line.lower()
            if "error" in line_lower or "failure" in line_lower:
                line = log.RED + line + log.END
            if "success" in line_lower:
                line = log.GREEN + line + log.END
            print("   " + log.GRAY + line + log.END)

def replace_in_file(filepath, text, replacement):
    input_file = open(filepath,'r')
    output_file = open(filepath + ".tmp", 'a')

    for line in input_file.readlines():
        output_file.write(line.replace(text, replacement))
    input_file.close()
    output_file.close()
    remove(filepath)
    os.rename(filepath + ".tmp", filepath)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
