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
    
def makeTestArrays(cursor, offset, labelarr, imgarr):
    o = offset*10    
    counter = 0
    for GardID, Sys_Filename, Img in cursor:
        if (counter < 10):        
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
        
        if (counter < 10):
            imgarr[counter+o] = smplmatx
            
        counter+=1
    return (labelarr, imgarr)
    
def padImages(img_matx, offset, rsize, csize):
    z_arr = np.zeros((rsize, csize), dtype = np.int)
    z_arr[:][:] = 255
#    print z_arr.shape
    (rows, cols) = img_matx.shape
#    print "rows = {}, cols = {}".format(rows,cols)
    
    if (rows % 2): #if odd
        rtemp = rows + 1
    else:
        rtemp = rows
        
    if (cols % 2):
        ctemp = cols + 1
    else:
        ctemp = cols
        
#    xtemp = xtemp / 2
#    ytemp = ytemp / 2
    
    c_start = (csize / 2) - (ctemp / 2)
    r_start = (rsize / 2) - (rtemp / 2)
#    print "c = {}, r = {}".format(c_start, r_start)
    
    for i in range(rows):
        for j in range(cols):
#            print "i = y = row = {}, j = x = col = {}".format(i,j)
            z_arr[r_start + i][c_start + j] = img_matx[i][j]
            
#    pad_array[offset] = z_arr
#    return pad_array
    return z_arr

if __name__ == '__main__':
    
    imgarr = [None]*40
    labelarr = [None]*40
    padarr = [None]*40
    
    (h,u,pw) = mysqlLogin('C:\Users\USER\Documents\mysqlid.txt')
    
    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
    some_ID = 'A1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
    
    (labelarr, imgarr) = makeTestArrays(cursor, 0, labelarr, imgarr)
  
    
    some_ID = 'D21'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
    
    print "WHUT"
    (labelarr, imgarr) = makeTestArrays(cursor, 1, labelarr, imgarr)
    
        
    some_ID = 'G1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    print "WHUT"
    (labelarr, imgarr) = makeTestArrays(cursor, 2, labelarr, imgarr)

    
    some_ID = 'O1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    print "WHUT"
    (labelarr, imgarr) = makeTestArrays(cursor, 3, labelarr, imgarr)
    
    print labelarr
    
    MaxX = 0
    MaxY = 0
    
    MinX = 1000
    MinY = 1000
    
    for i in range(len(imgarr)):
        (xdim, ydim) = imgarr[i].shape
        (MaxX, MaxY) = biggestDims(MaxX, MaxY, xdim, ydim)
        (MinX, MinY) = smallestDims(MinX, MinY, xdim, ydim)
        
    print "Maximum Dimensions in array: ({}, {})".format(MaxX, MaxY)
    print "Minimum Dimensions in array: ({}, {})".format(MinX, MinY)
    
    #set pixel dims of padded images
    xsize = 120
    ysize = 120
    
    for i in range(len(imgarr)):
        padarr[i] = padImages(imgarr[i], i, ysize, xsize)
        print "Success #{}".format((i+1))
        
    #Visualization of random elements
    # Get the figure and axes.
    fig, axes = pyplot.subplots(5, 5)
    axes = axes.reshape(25)
    fig.suptitle("Random Sampling of Glyphs")
    
    # Plot random images.
    indices = np.random.randint(len(padarr), size=25)
    for axis, index in zip(axes, indices):
        image = padarr[index]#[index, :, :]
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        axis.imshow(image, cmap = pyplot.cm.Greys_r)
        
            
        
    # Convert our data set into an easy format to use.
    # This is a list of (x, y) pairs. x is an image, y is a label.
#    dataset = []
#    for i in xrange(len(imgarr)):
#        dataset.append((imgarr[i], labelarr[i]))
#        
    