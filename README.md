# (Neo)vim Tmux Remote
A simple automation tool that utilize [Neovim Remote](https://github.com/mhinz/neovim-remote) to find a running vim instance in the currently active [Tmux](https://github.com/kovidgoyal/kitty) tab and send file there.

# Why?
Neovim-remote is great for it's purpose: opening file from the terminal into a vim window. But it doesn't have the capability to detect currently active neovim socket. This tool solve that problem by finding the first running neovim socket in the tmux window.

# Installation
run the following command
```sh
python3 -m pip install git+https://github.com/NikoKS/auto-nvr.git
```

***alternatively***
If you want to install it in a virtual environment to keep a clean global packages, use the `install.sh` and `uninstall.sh` script to install and uninstall. Note that [Poetry](https://github.com/python-poetry/poetry) is needed to use this script.
don't forget to add ~/.local/bin to your path

# Use case
1. Send file to existing Nvim window
The command needs to be run inside a tmux session
```sh
$ vir filename
```
2. Avoid nesting vim session when opening [lazygit](https://github.com/jesseduffield/lazygit) inside vim
This is honestly my main use case for this tool. Also needs to be inside tmux session.
to do this, add `vir` as your core.editor in git config OR set EDITOR=vir as an environment variable. Now, when pressing e to edit file inside lazygit, it would open the file on the existing vim window.

# Note
This tool is originally to be used with kitty terminal splits. I mainly use tmux now and no longger use neovim remote with kitty. The original tool can still be found in branch `kitty`
