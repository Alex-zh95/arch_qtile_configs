#!/bin/sh

DEVICE='UNIW0001:00 093A:0255 Touchpad'

enabled=$(xinput list-props "$DEVICE" | awk '/^\tDevice Enabled \([0-9]+\):\t[01]/ {print $NF}')
case $enabled in
    0)
        xinput enable "$DEVICE"
        echo "$DEVICE enabled"
        ;;
    1)
        xinput disable "$DEVICE"
        echo "$DEVICE disabled"
        ;;
    *)
        echo "Unable to determine state of $DEVICE"
        ;;
esac
