#!/bin/bash
dunst &
flameshot &
nitrogen --restore &
picom &
nm-applet &
xset s off -dpms &
xinput set-prop "DELL0957:00 06CB:CDD6 Touchpad" "libinput Tapping Enabled" 1 &
autorandr -c