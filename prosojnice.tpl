ffmpeg -f video4linux2 -vc 1 -tvstd pal -i /dev/video1 -r 1 -f image2 prosojnice/%03d.jpg
