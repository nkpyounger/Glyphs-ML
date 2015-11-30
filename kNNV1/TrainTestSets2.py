# -*- coding: utf-8 -*-

import MySQLdb as mariadb
from PIL import Image
import numpy as np
import StringIO
import sys
from matplotlib import pyplot

def mysqlLogin(filepath):
    myf = open(filepath, 'r')
    h = myf.readline()
    u = myf.readline()
    pw = myf.readline()
    
    h = h[:-1]
    u = u[:-1]
    pw = pw[:-1]
    
    return (h,u,pw)
    
def loadImg (binstring):
    bufimg = StringIO.StringIO(binstring)
    im = Image.open(bufimg)
    pix = im.load()
    bufimg.close()
    return (im, pix)
    
def makePixelArray(xdim, ydim, loadedimg):
    pxarray = []
    for j in range(ydim):
        for i in range(xdim):
            pxarray.append(list(loadedimg[i,j]))
    return pxarray
    
def checkMatrixReshape(xdim, ydim, pxmatrix, loadedimg):
    boolcheck = True
    for j in range(ydim):
        for i in range(xdim):
            if (np.array_equal(list(loadedimg[i,j]),pxmatrix[j][i])):
                continue
            else:
                 print "ERROR"   
                 print list(loadedimg[i,j])
                 print pxmatrix[i][j]
                 boolcheck = False
                 #add more useful error info?
    return boolcheck
    
def checkRGBVals(xdim, ydim, pxmatrix):
    boolcheck = True
    for i in range(xdim):
        for j in range(ydim):
            if (pxmatrix[j][i][0] == pxmatrix[j][i][1] and pxmatrix[j][i][0] == pxmatrix[j][i][2]):
                continue
            else:
                print "error"
                print pxmatrix[j][i]
                print "at {}, {}".format(j,i) 
                boolcheck = False
                #add more useful error info?
    return boolcheck
    
def collapseMatrix(xdim, ydim, pxmatrix):
    smplmatx = np.zeros((ydim,xdim), dtype=np.int)
#        print type(smplmatx[0][0])
    
#        print "OVERWRITE matrix of pixels"            
    for i in range(xdim):
        for j in range(ydim):
            smplmatx[j][i] = pxmatrix[j][i][0]
    return smplmatx
    
def setImgMode(openimg):    
    if (openimg.mode == "RGB"):
        p = 3
    elif (openimg.mode == "RGBA"):
        p = 4
    else:
        sys.exit(1)
    return p
    
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
    
def makeTestArrays(cursor, offset, labelarr, imgarr, num_examples):
    o = offset*num_examples    
    counter = 0
    for GardID, Sys_Filename, Img in cursor:
        if (counter < num_examples):        
            labelarr[counter+o] = GardID        
        
        (im, pix) = loadImg(cursor.fetchone()[2])
        (xmax, ymax) = im.size
        p = setImgMode(im)
        
        pxarray = makePixelArray(xmax, ymax, pix)
        
        pxmatrix = np.reshape(pxarray, (ymax, xmax, p))

        pxerr = checkMatrixReshape(xmax, ymax, pxmatrix, pix)
        if not pxerr:
            sys.exit(1)
       
        rgberr = checkRGBVals(xmax, ymax, pxmatrix)
        if not rgberr:
            continue
 
        smplmatx = collapseMatrix(xmax, ymax, pxmatrix)
        
        if (counter < num_examples):
            imgarr[counter+o] = smplmatx
            
        counter+=1
        # break out of loop and allow use of remaining images in subsequent
        # arrays
        if counter >= num_examples:
            return (labelarr, imgarr)
    return (labelarr, imgarr)
    
def BuildArrays():
    
    (h,u,pw) = mysqlLogin('/home/nyounger/Documents/mysqlid.txt')
    
    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
    
    # Set up training and testing sets with 30 and 10 (respectively)
    # glyphs from Aa1, D36, G1, M17 (and source: EG-W)
    SIGN_TYPES = 4
    trainimg = [None]*30*SIGN_TYPES
    trainlbl = [None]*30*SIGN_TYPES
    testimg = [None]*10*SIGN_TYPES
    testlbl = [None]*10*SIGN_TYPES
    
#    print len(trainimg)
#    print len(testimg)
    
    some_ID = 'Aa1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    (trainlbl, trainimg) = makeTestArrays(cursor, 0, trainlbl, trainimg, 30)
#    for GardID, Sys_FileName, Img in cursor:
#        print Sys_FileName
    (testlbl, testimg) = makeTestArrays(cursor, 0, testlbl, testimg, 10)
    
    some_ID = 'D36'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    (trainlbl, trainimg) = makeTestArrays(cursor, 1, trainlbl, trainimg, 30)
    (testlbl, testimg) = makeTestArrays(cursor, 1, testlbl, testimg, 10)
    
    some_ID = 'G1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    (trainlbl, trainimg) = makeTestArrays(cursor, 2, trainlbl, trainimg, 30)
    (testlbl, testimg) = makeTestArrays(cursor, 2, testlbl, testimg, 10)
    
    some_ID = 'M17'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    (trainlbl, trainimg) = makeTestArrays(cursor, 3, trainlbl, trainimg, 30)
    (testlbl, testimg) = makeTestArrays(cursor, 3, testlbl, testimg, 10)
    
    return (trainlbl, trainimg, testlbl, testimg)
    
#    print trainlbl
#    print testlbl
#    
#    #Visualization of random elements
#    # Get the figure and axes.
#    fig, axes = pyplot.subplots(5, 5)
#    axes = axes.reshape(25)
#    fig.suptitle("Random Sampling of Glyphs")
#    
#    # Plot random images.
#    indices = np.random.randint(len(trainimg), size=25)
#    for axis, index in zip(axes, indices):
#        image = trainimg[index]#[index, :, :]
#        axis.get_xaxis().set_visible(False)
#        axis.get_yaxis().set_visible(False)
#        axis.imshow(image, cmap = pyplot.cm.Greys_r)
    
    
    mariadb_connection.close()

