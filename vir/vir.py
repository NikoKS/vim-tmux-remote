import nvr
import fire
import psutil
from typing import List
from pathlib import Path
from subprocess import run
from termcolor import colored, cprint

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
    """Given the pid, get the servername of the running nvim instance
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


def detect_nvim_pid() -> int:
    """Detect the pid of running nvim process in current tmux tab
    Returns:
        int: pid if succesfull 0 if nvim not found
    """
    cmd = "tmux list-panes -F '#{pane_pid},#{pane_title}'"
    panes = run(cmd, shell=True, capture_output=True, text=True).stdout
    
    pid = 0
    for pane in panes.split("\n"):
        if 'NVIM' in pane or 'nvim' in pane:
            pid = int(pane.split(',')[0])
            break
    
    if pid:
        for proc in psutil.Process(pid).children():
            if proc.name() == 'nvim':
                return(int(proc.pid))
        pid = 0

    return(pid)


def send(filename: str):
    """Send file to the current running vim instance in the active kitty tab
    Args:
        filename (str): filename to send to vim
    """
    filepath = Path(filename)

    if filepath.is_dir():
        cprint(f'{filename} is a directory', 'yellow')
        exit(0)
    elif not filepath.is_file():
        cprint(f"\n{filename} doesn't exist, opening new file", 'green')

    pid = detect_nvim_pid()
    if not pid:
        cprint(f'No running vim instance detected. Creating new vim window', 'green')
        exit(0)

    server = get_nvim_server(pid)
    nvr.main(argv=('--nostart', '--servername', server,
                   '--remote-silent', '-l', str(filepath)))

def main():
    fire.core.Display = Display
    fire.Fire(send)
