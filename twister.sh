#!/bin/sh

# get the real script path
script_path=`readlink -n $0`
if [ $? -ne 0 ]; then
    script_path="$0"
fi

# cd to the twister directory
cd `dirname $script_path`

# start twister
python twister.py "$@"