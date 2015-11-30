# -*- coding: utf-8 -*-

import MySQLdb as mariadb
from PIL import Image
import numpy as np
import StringIO
import sys
from matplotlib import pyplot
import TrainTestSets2 as tts #dash in name produces 'invalid syntax'

def biggestDims(MaxX, MaxY, xdim, ydim):
    if (xdim > MaxX):
        MaxX = xdim
#        print "({}, {})".format(MaxX, MaxY)
            
    if (ydim > MaxY):
        MaxY = ydim
#        print "({}, {})".format(MaxX, MaxY)
            
    return (MaxX, MaxY)
    
def smallestDims(MinX, MinY, xdim, ydim):
    if (xdim < MinX):
        MinX = xdim
#        print "({}, {})".format(MaxX, MaxY)
            
    if (ydim < MinY):
        MinY = ydim
#        print "({}, {})".format(MaxX, MaxY)
            
    return (MinX, MinY)

def SetPaddingSize(trainlbl, trainimg, testlbl, testimg):
#    (trainlbl, trainimg, testlbl, testimg) = tts.BuildArrays()
#    print trainlbl
    
    MaxX = 0
    MaxY = 0
    
    MinX = 1000
    MinY = 1000
    
    for i in range(len(trainimg)):
        (xdim, ydim) = trainimg[i].shape
        (MaxX, MaxY) = biggestDims(MaxX, MaxY, xdim, ydim)
        (MinX, MinY) = smallestDims(MinX, MinY, xdim, ydim)
    
    for i in range(len(testimg)):
        (xdim, ydim) = testimg[i].shape
        (MaxX, MaxY) = biggestDims(MaxX, MaxY, xdim, ydim)
        (MinX, MinY) = smallestDims(MinX, MinY, xdim, ydim)
        
#    print "Maximum Dimensions in array: ({}, {})".format(MaxX, MaxY)
#    print "Minimum Dimensions in array: ({}, {})".format(MinX, MinY)
    
    #padimages code presumes even dimensions (i think...)
    if MaxX % 2: #if odd
        xpad = MaxX + 3
    else:
        xpad = MaxX + 2
        
    if MaxY %2:
        ypad = MaxY + 3
    else:
        ypad = MaxY + 2
        
    return (xpad, ypad)