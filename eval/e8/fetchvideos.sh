#! /bin/bash

RATE_LIMIT='400k'
HEIGHT='480'
YOUTUBE="https://www.youtube.com/watch?v="
OUTDIR="videos"
VID_IDS=(
'-MBS2YvUY2M'
)
LOGFILE='.download.log'

for vid in "${VID_IDS[@]}"
do
  echo "=== Downloading video $vid ==="
  youtube-dl \
    --rate-limit $RATE_LIMIT \
    -f "best[height=$HEIGHT]+bestaudio" \
    -o "videos/%(autonumber)s-%(id)s-%(title)s.%(ext)s" \
    --autonumber-size 1 \
    --restrict-filenames \
    --no-overwrites \
    "$YOUTUBE$vid" \
    2>&1 | tee -a $LOGFILE
done
