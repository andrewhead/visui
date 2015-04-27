#! /bin/bash

RATE_LIMIT='400k'
HEIGHT='480'
YOUTUBE="https://www.youtube.com/watch?v="
OUTDIR="videos"
VID_IDS=(
'I1HpEzxYHxE'
'B0sCahhT_A4'
'XKBJKS84UYI'
'vXcC533_IcQ'
'f0Ddy4R_-_A'
'NkxADI58MKw'
'Z149x12sXsw'
'lVjCMXQGS_w'
'nqFpfrUrMM4'
'SVZ1P35xgNQ'
'VKvFhNqcr9M'
'o1vRJ07KDZ0'
'-b5ZLwhjwY0'
'Uen8B9p05tI'
'-MBS2YvUY2M'
'm20n_GAsCtM'
'K25KMQOnhjQ'
'p9KRJoX13vo'
'94dXuNQRNh8'
'4O8bW4PD8bA'
)

for vid in "${VID_IDS[@]}"
do
  echo "=== Downloading video $vid ==="
  youtube-dl \
    --rate-limit $RATE_LIMIT \
    -f "best[height=$HEIGHT]+bestaudio" \
    -o "videos/V%(id)s-%(title)s-%(format)s.%(ext)s" \
    --restrict-filenames \
    --no-overwrites \
    "$YOUTUBE$vid"
done
