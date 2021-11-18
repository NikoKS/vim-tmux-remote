#!/bin/bash
cd "$(dirname "$0")"

poetry install
bin=`poetry env list --full-path | cut -d\  -f1`/bin/vir
local_bin=$HOME/.local/bin/
mkdir -p $local_bin
ln -sf $bin $local_bin/vir
