#! /bin/bash

RATE_LIMIT='400k'
HEIGHT='480'
YOUTUBE="https://www.youtube.com/"
TARGET="playlist?list=PLF03C6B2C0B292A1E"
OUTDIR="videos"
LOGFILE=".download.log"

youtube-dl \
  --rate-limit $RATE_LIMIT \
  -f "best[height=$HEIGHT]+bestaudio" \
  -o "videos/%(autonumber)s-%(id)s-%(title)s.%(ext)s" \
  --restrict-filenames \
  --no-overwrites \
  --ignore-errors \
  $YOUTUBE$TARGET \
  2>&1 | tee -a $LOGFILE
