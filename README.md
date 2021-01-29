# Auto Neovim Remote
A simple automation tool that utilize [Neovim Remote](https://github.com/mhinz/neovim-remote) to find a running vim instance in the currently active [Kitty Terminal](https://github.com/kovidgoyal/kitty) tab and send file there.

# Why?
neovim-remote is great since it's making the terminal more IDE like. But I only have one realistic use case for it that is sending file to a running nvim window. And usually I have multiple running nvim in different terminal tab. It's hard to keep track the servername and having to specify different nvim servername at start.

So this script automates that headache so you can run nvim without specifying the adrress and it will find a running nvim in the current tab (only works for kitty terminal but the idea should be easily translatable to other terminal)

# Installation
run the following command
```
python3 -m pip install git+https://github.com/NikoKS/auto-nvr.git
```

# Usage
The command needs kitty remote control feature to be turned on to work as it depends on it to find the nvim process and move focus window
```
$ vir filename
```
Yeah... that's it, or add the -n flag for no-focus so it doesn't change the focus window.
```
$ vir -n filename
```
