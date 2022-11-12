#!/bin/python
'''
File:           tmux_init.py

Checks for existing tmux sessions and opens the last session should it exist.
'''

import subprocess

session_text = subprocess.run(['tmux', 'ls'], capture_output=True, encoding='utf-8').stdout

if session_text=="":
    subprocess.run(['tmux'])
else:
    subprocess.run(['tmux', 'a'])
