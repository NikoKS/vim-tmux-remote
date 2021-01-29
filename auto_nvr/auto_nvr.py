"""
run neovim remote into the nvim server in the currently active kitty tab

workflow :
    - find which window has vim in the current tab:
        if current tab doesn't have vim. exit gracefully with a message
        if current tab have vim, get the pid of the first vim process it finds.
    - find out the servername for NVIM using psutil pid
    - run nvr --remote on the servername it found.
"""

from termcolor import colored, cprint
from typing import List, Tuple
from pathlib import Path
import subprocess
import psutil
import yaml
import fire
import nvr


def Display(content: List[str], out):
    """ Function for replacing the default python-fire Display """
    keywords = ('name', 'synopsis', 'description', 'positional arguments',
                'flags', 'notes')
    keywords = set(colored(key.upper(), attrs=['bold']) for key in keywords)

    lines = content[0].splitlines()
    for line in lines:
        if line in keywords:
            out.write(colored(line, 'green'))
        else:
            out.write(line)
        out.write('\n')


def get_nvim_server(pid: int) -> str:
    """ given the pid, get the servername of the running nvim instance
    Args:
        pid (int): nvim process id
    Returns:
        str: unix servername from the given pid
    """
    nvim_process = psutil.Process(pid)
    for conn in nvim_process.connections('unix'):
        if conn.laddr:
            return conn.laddr
    cprint(f'Failed to get nvim servername from process pid {pid}', 'yellow')
    exit(0)


def detect_nvim_pid() -> Tuple[int, int]:
    """ Detect if there's a running nvim process in the current kitty tab
    Returns:
        tuple: a tuple containing the nvim pid and window pid
    """
    ls = subprocess.run('kitty @ ls', shell=True, capture_output=True)
    kitty_state = yaml.load(ls.stdout, Loader=yaml.FullLoader)

    def find_active_tab(kitty_state: List):
        for session in kitty_state:
            for tab in session['tabs']:
                if tab['is_focused']:
                    return tab
        cprint('Failed to find active tab', 'yellow')
        exit(0)

    tab = find_active_tab(kitty_state)
    for window in tab['windows']:
        for process in window['foreground_processes']:
            if 'nvim' in process['cmdline']:
                return(process['pid'], window['pid'])
    cprint('Failed to find nvim in the current active kitty tab', 'yellow')
    exit(0)


def send(filename: str, no_focus=False):
    """send file to the current running vim instance in the active kitty tab

    Args:
        filename (str): filename to send to vim
        no_focus (bool): -n set this flag to make the focus window to stay at
            current window
    """
    filepath = Path(filename)
    if filepath.is_dir():
        cprint(f'{filename} is a directory', 'yellow')
        exit(0)
    elif not filepath.is_file():
        cprint(f"\n{filename} doesn't exist, opening new file", 'green')
    pid, wpid = detect_nvim_pid()
    server = get_nvim_server(pid)
    nvr.main(argv=('--nostart', '--servername', server,
                   '--remote', str(filepath)))
    if not no_focus:
        subprocess.run(f'kitty @ focus-window --match pid:{wpid}', shell=True)


def main():
    fire.core.Display = Display
    fire.Fire(send)
