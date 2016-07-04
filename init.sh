#!/bin/bash
#

trap '' SIGINT
base_dir=$(dirname $0)

export LANG='zh_CN.UTF-8'
$base_dir/venv/bin/python $base_dir/connect.py

exit