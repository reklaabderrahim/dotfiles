#!/usr/bin/env bash

# Terminate already running conky instances
killall -q conky

# Launch conky
echo "---" | tee -a /tmp/conky.log
conky -c ~/.config/conky/tomorrow-night-01.conkyrc 2>&1 | tee -a /tmp/conky.log & disown

echo "Bar launched..."
