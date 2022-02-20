#!/bin/sh


isHdmi=`/usr/bin/xrandr | /usr/bin/grep -i " connected" | awk '{print $1}' | tail -n 1`
echo $isHdmi
output="HDMI-1-0"

if [ $isHdmi == $output ]; then
	sleep 2 && tint2 -c ~/.config/tint2/i3/tint2rc & 
	sleep 2 && tint2 -c ~/.config/tint2/i3/2-tint2rc &
	sleep 2 && tint2 -c ~/.config/tint2/i3/3-tint2rc &
else
	sleep 2 && tint2 -c ~/.config/tint2/i3/tint2rc
fi
