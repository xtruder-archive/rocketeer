while [ 1 ]; do
	for i in prosojnice/0*
	do
		echo 1 > /dev/null
	done
	echo $i
	rm prosojnice/live.jpg
	ln -s $i prosojnice/live.jpg
	sleep .3
done
