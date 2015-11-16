# -*- coding: utf-8 -*-

# https://mariadb.com/blog/how-connect-python-programs-mariadb
# http://conda.pydata.org/docs/using/pkgs.html#install-a-package

# ^ all i needed - simple conda install, no external dl required

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


if __name__ == '__main__':
    
    imgarr = [None]*40
    labelarr = [None]*40
      
    
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
    
    
    outf2 = open('T40GOutputFull.txt', 'w')
    outf2.write(' '.join(map(str, imgarr)))
    outf2.close
    
    print labelarr
    
    #Visualization of random elements
    # Get the figure and axes.
    fig, axes = pyplot.subplots(5, 5)
    axes = axes.reshape(25)
    fig.suptitle("Random Sampling of Glyphs")
    
    # Plot random images.
    indices = np.random.randint(len(imgarr), size=25)
    for axis, index in zip(axes, indices):
        image = imgarr[index]#[index, :, :]
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        axis.imshow(image, cmap = pyplot.cm.Greys_r)
        
    mariadb_connection.close()