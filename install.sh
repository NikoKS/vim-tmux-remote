#!/bin/bash
cd "$(dirname "$0")"

poetry install
bin=`poetry env list --full-path | cut -d\  -f1`/bin/
local_bin=$HOME/.local/bin/
mkdir -p $local_bin
ln -sf $bin/vir $local_bin/vir
ln -sf $bin/nvr $local_bin/nvr
