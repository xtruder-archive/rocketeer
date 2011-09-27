ffmpeg -f video4linux2 -vc 1 -tvstd pal -i /dev/video0 -f alsa -i hw:0,0,0 -acodec libfaac -ab 96k -ac 2 \
	-vcodec libx264 -preset fast \
	-vf crop=in_w-2*8:in_h-2*6,yadif,scale=-1:576,hqdn3d -vb 600k -maxrate 600k -bufsize 700k -r 25 -s {{resolution}} \
	-threads 0  -vbsf h264_mp4toannexb -f mpegts \
	udp://maat.viidea.com:5000?pkt_size=1316 -target pal-dv -threads 0 dump/{{dumpfile}}
