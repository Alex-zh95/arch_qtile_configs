#!/bin/python
import subprocess
import re

print('installer.py will install all non-commented packages in your installers.x86_64 file')
pkg_cmd_str = 'yay -S'

try:
    pkgs = open('packages.x86_64', 'r')
except FileNotFoundError:
    print('installer.py - Error: Cannot locate packages.x86_64 in current directory.')
    exit(1)

# If yay is not installed, first install it!
if subprocess.run(['pacman', '-Qi', 'yay']).returncode > 0:
    print('installer.py: Need to first install yay')
    print('installer.py: Assuming we can install yay-bin from pacman (e.g. via Arco repos')
    yay_sts = subprocess.run(['sudo', 'pacman', '-S', 'yay-bin'])

    if yay_sts.returncode > 0:
        print('installer.py - Error: Failed to install yay-bin')
        exit(2)

count = 0

# Read line by line, appending to pkg_list
while True:
    # Get current line
    ln = pkgs.readline()

    # Append to pkg_cmd_str if does not begin with '#'
    if not ln.startswith('#'):
        count += 1

        # Remove all line break chars
        ln = re.sub('\n', '', ln)
        pkg_cmd_str = f'{pkg_cmd_str} {ln}'

        print(f'installer.py: Found {count} packages in file...', flush=True)
    
    if 'EOF' in ln:
        break

pkgs.close()

pkg_cmd_str = f'{pkg_cmd_str} --noconfirm --needed'
print(pkg_cmd_str)

pkg_cmd = pkg_cmd_str.split(sep=' ')
run_proc = subprocess.run(pkg_cmd)

status = 'installer.py: Done.' if run_proc.returncode == 0 else 'installer.py: Install errors - check above output from yay/pacman'
print(status)
