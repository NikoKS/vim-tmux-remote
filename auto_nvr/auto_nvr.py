"""
run neovim remote into the nvim server in the currently active kitty tab

workflow :
    - find which window has vim in the current tab:
        if current tab doesn't have vim. exit gracefully with a message
        if current tab have vim, get the pid of the first vim process it finds.
    - find out the servername for NVIM using psutil pid
    - run nvr --remote on the servername it found.
"""

from pathlib import Path
from typing import List
import subprocess
import psutil
import yaml
import fire
import nvr


def get_nvim_server(pid: int) -> str:
    """ given the pid, get the servername of the running nvim instance """
    nvim_process = psutil.Process(pid)
    for conn in nvim_process.connections('unix'):
        if conn.laddr:
            return conn.laddr
    print(f'Failed to get nvim servername from process pid {pid}')
    exit(0)


def detect_nvim_pid() -> int:
    """ Detect if there's a running nvim process in the current kitty tab """
    ls = subprocess.run('kitty @ ls', shell=True, capture_output=True)
    kitty_state = yaml.load(ls.stdout, Loader=yaml.FullLoader)

    def find_active_tab(kitty_state: List):
        for session in kitty_state:
            for tab in session['tabs']:
                if tab['is_focused']:
                    return tab
        print('Failed to find active tab')
        exit(0)

    tab = find_active_tab(kitty_state)
    for window in tab['windows']:
        for process in window['foreground_processes']:
            if 'nvim' in process['cmdline']:
                return(process['pid'])
    print('Failed to find nvim in the current active kitty tab')
    exit(0)


def send(filename: str):
    filepath = Path(filename)
    # TODO: Check if path exist
    pid = detect_nvim_pid()
    server = get_nvim_server(pid)
    print(server)
    print(type(server))
    print(filepath)
    nvr.main(argv=('--nostart', '--servername', server,
                   '--remote', str(filepath)))


def main():
    fire.Fire(send)
