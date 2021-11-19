# (Neo)vim Tmux Remote
A simple automation tool that utilize [Neovim Remote](https://github.com/mhinz/neovim-remote) to find a running vim instance in the currently active [Tmux](https://github.com/kovidgoyal/kitty) tab and send file there.

# Why?
Neovim-remote is great for it's purpose: opening file from the terminal into a vim window. But it doesn't have the capability to detect currently active neovim socket. This tool solve that problem by finding the first running neovim socket in the tmux window.

# Installation
run the following command
```sh
python3 -m pip install git+https://github.com/NikoKS/auto-nvr.git
```

**Alternatively**

If you want to install it in a virtual environment to keep a clean global packages, use the `install.sh` and `uninstall.sh` script to install and uninstall. Note that [Poetry](https://github.com/python-poetry/poetry) is needed to use this script.
don't forget to add ~/.local/bin to your path

# Usage
The command needs to be run inside a tmux session
```sh
$ vir filename
```

# History
This tool is originally to be used with kitty terminal splits. I mainly use tmux now and no longger use neovim remote with kitty. The original tool can still be found in branch `kitty`
