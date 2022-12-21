#!/bin/sh

# Automate the screens.py script by looking for all connected monitors, excluding built-in (designated here by "eDP-x",
# printing out the list of these as comma-separated values and passing as argument into screen.py's -o flag
/bin/python3 ~/.config/qtile/screens.py -o "$(xrandr -q | grep -E "[^dis]connected" | grep -v "^[eDP]" | awk '{ printf "%s%s", sep, $1; sep=", " } END{print ""}')"
