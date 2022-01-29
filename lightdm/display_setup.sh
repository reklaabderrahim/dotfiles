#!/bin/bash

/usr/bin/setxkbmap fr

isHdmi=`/usr/bin/xrandr | /usr/bin/grep -i " connected" | awk '{print $1}' | tail -n 1`
echo $isHdmi
output="HDMI-1-0"

if [ $isHdmi == $output ]; then
   /usr/bin/xrandr --output eDP-1 --dpi 142 --primary --mode 1920x1080 --pos 2560x255 --rotate normal --output DP-1 --off --output HDMI-1-0 --dpi 108 --mode 2560x1440 --pos 0x0 --rotate normal
else
    /usr/bin/xrandr --output eDP-1 --dpi 108 --primary --mode 1920x1080 --rotate normal
fi
