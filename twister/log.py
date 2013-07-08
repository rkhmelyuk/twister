# -*- coding: utf8 -*-

HEADER = '\033[35m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
CYAN = '\033[36m'
GRAY = '\033[37m'
END = '\033[0m'

def write(text):
    print text

def title(title):
    print HEADER + ("[ %s ]" % title).ljust(80, '-') + END

def info(message):
    print("[" + GREEN + "INFO" + END + "]  %s" % message)

def warn(message):
    print("[" + YELLOW + "WARN" + END + "]  %s" % message)

def error(message):
    print("[" + RED + "ERROR" + END + "] %s" % message)

def help(message):
    print(HEADER + "Hint:   " + END + message)

def command(cmd):
    return CYAN + "twister %s" % cmd + END