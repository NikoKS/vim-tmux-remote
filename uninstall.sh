#!/bin/bash
cd "$(dirname "$0")"

env=`poetry env list | cut -d\  -f1`
poetry env remove $env
local_bin=$HOME/.local/bin/
rm $local_bin/vir
