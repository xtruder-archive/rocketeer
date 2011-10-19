#!/bin/python
import math, operator, sys, getopt
from PIL import Image

def compare(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add,
        map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return rms

def FrameColerate( frames1, frames2 ):
    frame1_counter= 0
    frame2_counter= 0
    min_sum= sys.maxint
    offset= 0

    while (frame1_counter+len(frames2))<len(frames1):
        for frame2_counter in range(0,len(frames2)):
            sum+= compare(frames1[frame1_counter], frames2[frame2_counter])
        if sum<min_sum:
            min_sum= sum
            offset= frame1_counter

        sum= 0
        frame1_counter+= 1

    return offset

if __name__ == "__main__":
    optlist, args = getopt.getopt(sys.argv[1:], 'a:b:')

    frames1= None
    frames2= None
    for (key,val) in optlist:
        if key=='a':
            frames1= val
        if key=='b':
            frames2=val

    if frames1 and frames2:
        print FrameColerate( frames1, frames2 )
    else:
        print "-1"
