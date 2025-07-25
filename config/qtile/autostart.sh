#!/bin/sh
#feh --bg-scale /home/concerned_penguin/Downloads/bg.png

# Start picom compositor
picom --config ~/.config/picom/picom.conf --xrender-sync-fence &

#pywal 
wal -R &
# Restart Qtile to apply colors
qtile cmd-obj -o cmd -f restart
#wal -R(for manual or load old colors as last time)

#for 144hz
xrandr --output DP-2 --mode 1920x1080 --rate 144.10

