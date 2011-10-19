#!/bin/bash
echo "Extracting frames from first video"
ffmpeg -y -i $1 -vframes 1500 -an -sameq -f image2 -r 25 frames1-%03d.jpg # extract 60 seconds
echo "Extracting frames from second video"
ffmpeg -y -i $2 -vframes 30 -an -sameq -f image2 -r 25 frames2-%3d.jpg # extract 60 seconds

echo "Colerating videos. Using frames from second video to find frame in first"

