#!/usr/bin/env bash 

/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
picom --config ~/.config/picom/picom-blur.conf --experimental-backends &
dunst &
flameshot &
$HOME/.config/conky/launch.sh &
volumeicon &
nm-applet &
#pamac-tray &
blueberry-tray &
nitrogen --restore &

