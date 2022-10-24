#!/bin/python

###########################################################################################
# PROJECT TO EXTERNAL SCREEN
# 
# Python script to project to externally connected screen(s). 
# Default to HDMI output at 1080p at 2x2 scaling
###########################################################################################

import argparse
import os

# Accept various inputs
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputs', default='HDMI-1', help='List all the output IDs, separated by spaces', type=str)
parser.add_argument('-r', '--resolution' , default='1920x1080', help='Resolution for outputs', type=str)
parser.add_argument('-d', '--dock_only', default='False', help='Set to True to switch off main laptop display', type=str)

args = parser.parse_args()

# Tidy up the output screen identifiers
list_outputs = args.outputs.split(', ')

# Build the output string
# --output list_outputs[0] --output list_outputs[1] ... 

# If docking is specified, then we turn off the laptop display
output_str = 'xrandr --output eDP-1 --off' if args.dock_only == 'True' else 'xrandr'

# We need to arrange the screens in horizontal layout given
anchor = args.resolution.split('x')

# Beware of the scaling factor!
list_xPos = [int(anchor[0])*2*n for n in range(len(list_outputs))]

for i in range(len(list_outputs)):
    # Add also the resolution, position, rotation and scaling
    output = list_outputs[i]
    position_str = f'{list_xPos[i]}x0'
    output_str = f'{output_str} --output {output} --mode {args.resolution} --pos {position_str} --rotate normal --scale 2x2'

    if i == 0:
        output_str = f'{output_str} --primary'

if args.dock_only == 'False':
    output_str = f'{output_str} --output eDP-1 --left-of {list_outputs[0]}'

# Apply the command built in output_str
print(f'Executing {output_str}')
st = os.system(output_str)

# Error checks - if any failure (i.e. st code above 0), then revert 
if st > 0:
    os.system(r'xrandr --output eDP-1 --primary --mode 2880x1800 --pos 0x0 --rotate normal')
    print('Error in detecting screens')

# Redraw wallpapers with feh
# This executes ./fehbg from within the home directory
redraw_bg = r'~/.fehbg &'
os.system(redraw_bg)
