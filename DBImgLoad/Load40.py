# -*- coding: utf-8 -*-

# https://mariadb.com/blog/how-connect-python-programs-mariadb
# http://conda.pydata.org/docs/using/pkgs.html#install-a-package

# ^ all i needed - simple conda install, no external dl required

import MySQLdb as mariadb
from PIL import Image
import numpy as np
import StringIO
import sys

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
    for i in range(xdim):
        for j in range(ydim):
            pxarray.append(list(loadedimg[i,j]))
    return pxarray
    
def checkMatrixReshape(xdim, ydim, pxmatrix, loadedimg):
    boolcheck = True
    for i in range(xdim):
        for j in range(ydim):
            if (np.array_equal(list(loadedimg[i,j]),pxmatrix[i][j])):
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
            if (pxmatrix[i][j][0] == pxmatrix[i][j][1] and pxmatrix[i][j][0] == pxmatrix[i][j][2]):
                continue
            else:
                print "error"
                print pxmatrix[i][j]
                print "at {}, {}".format(i,j) 
                boolcheck = False
                #add more useful error info?
    return boolcheck
    
def collapseMatrix(xdim, ydim, pxmatrix):
    smplmatx = np.zeros((xdim,ydim), dtype=np.int)
#        print type(smplmatx[0][0])
    
#        print "OVERWRITE matrix of pixels"            
    for i in range(xdim):
        for j in range(ydim):
            smplmatx[i][j] = pxmatrix[i][j][0]
    return smplmatx


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
        #cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'"%(some_ID))        
        # NEED single quotation marks around %s => '%s'
        # also "..."%(...) PERCENTsign NEEDEDor get typeerror http://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    #IDs with >=10 symbols: A1, Aa1, Aa13, D21, D36, D46, D58, G1, ...
        #G17, G43, I9, M17, M17x, N29, N35, N37, O1, O34, Q3, S29 ...
        #V1, V28, V31, W11, X1
    
    print "WHUT"
       
    #outf = open('L40Output.txt', 'w')       
    # the following works to load img from db into program for manip
    # https://docs.python.org/2/library/stringio.html
    # http://effbot.org/imagingbook/image.htm - see discussion under Image.fromstring
    counter = 0
    for GardID, Sys_Filename, Img in cursor:
        if (counter < 10):        
            labelarr[counter] = GardID        
        
        (im, pix) = loadImg(cursor.fetchone()[2])
        print im.size
        (xmax, ymax) = im.size
        print im.size
#        print pix[30,23]
        print im.mode
        if (im.mode == "RGB"):
            p = 3
        elif (im.mode == "RGBA"):
            p = 4
        
        pxarray = makePixelArray(xmax, ymax, pix)
        
        #print pxarray
        print (xmax*ymax)
        print len(pxarray)
        
        pxmatrix = np.reshape(pxarray, (xmax, ymax, p))
        print pxmatrix.shape
        
        print "pixel check"
        pxerr = checkMatrixReshape(xmax, ymax, pxmatrix, pix)
        if not pxerr:
            sys.exit(1)
        print "AYOKAY!"
        
        print "RGB Check"
        rgberr = checkRGBVals(xmax, ymax, pxmatrix)
        if not rgberr:
            continue
        print "OKEYDOKE"
        
        print "Simplify Matrix RGB Vals"
        smplmatx = collapseMatrix(xmax, ymax, pxmatrix)
                
#        print smplmatx[20][20]
#        print pix[20,20]
        
        if (counter < 10):
            imgarr[counter] = smplmatx
        
        #outf.write("\nIMAGE MATRIX\n")
        #outf.write(' '.join(map(str, smplmatx)))
        
        counter+=1
    #outf.close
    
    
    some_ID = 'D21'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
        #cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'"%(some_ID))        
        # NEED single quotation marks around %s => '%s'
        # also "..."%(...) PERCENTsign NEEDEDor get typeerror http://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    #IDs with >=10 symbols: A1, Aa1, Aa13, D21, D36, D46, D58, G1, ...
        #G17, G43, I9, M17, M17x, N29, N35, N37, O1, O34, Q3, S29 ...
        #V1, V28, V31, W11, X1
    
    print "WHUT"
       
    #outf = open('L40Output.txt', 'w')       
    # the following works to load img from db into program for manip
    # https://docs.python.org/2/library/stringio.html
    # http://effbot.org/imagingbook/image.htm - see discussion under Image.fromstring
    counter = 0
    for GardID, Sys_Filename, Img in cursor:
        if (counter < 10):
            labelarr[counter+10] = GardID        
        
        (im, pix) = loadImg(cursor.fetchone()[2])
        print im.size
        (xmax, ymax) = im.size
        print im.size
#        print pix[30,23]
        print im.mode
        print type(im.mode)
        
        if (im.mode == "RGB"):
            p = 3
        elif (im.mode == "RGBA"):
            p = 4
        
        pxarray = makePixelArray(xmax, ymax, pix)
        
        #print pxarray
        print (xmax*ymax)
        print len(pxarray)
        
        pxmatrix = np.reshape(pxarray, (xmax, ymax, p))
        print pxmatrix.shape
        
        print "pixel check"
        pxerr = checkMatrixReshape(xmax, ymax, pxmatrix, pix)
        if not pxerr:
            sys.exit(1)
        print "AYOKAY!"
        
        print "RGB Check"
        rgberr = checkRGBVals(xmax, ymax, pxmatrix)
        if not rgberr:
            continue
        print "OKEYDOKE"
        
        print "Simplify Matrix RGB Vals"
        smplmatx = collapseMatrix(xmax, ymax, pxmatrix)
                
#        print smplmatx[20][20]
#        print pix[20,20]
        
        if (counter < 10):
            imgarr[counter+10] = smplmatx
        
        #outf.write("\nIMAGE MATRIX\n")
        #outf.write(' '.join(map(str, smplmatx)))
        
        counter+=1
        
    some_ID = 'G1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
        #cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'"%(some_ID))        
        # NEED single quotation marks around %s => '%s'
        # also "..."%(...) PERCENTsign NEEDEDor get typeerror http://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    #IDs with >=10 symbols: A1, Aa1, Aa13, D21, D36, D46, D58, G1, ...
        #G17, G43, I9, M17, M17x, N29, N35, N37, O1, O34, Q3, S29 ...
        #V1, V28, V31, W11, X1
    
    print "WHUT"
       
    #outf = open('L40Output.txt', 'w')       
    # the following works to load img from db into program for manip
    # https://docs.python.org/2/library/stringio.html
    # http://effbot.org/imagingbook/image.htm - see discussion under Image.fromstring
    counter = 0
    for GardID, Sys_Filename, Img in cursor:
        if (counter < 10):
            labelarr[counter+20] = GardID        
        
        (im, pix) = loadImg(cursor.fetchone()[2])
        print im.size
        (xmax, ymax) = im.size
        print im.size
#        print pix[30,23]
        
        if (im.mode == "RGB"):
            p = 3
        elif (im.mode == "RGBA"):
            p = 4
        
        pxarray = makePixelArray(xmax, ymax, pix)
        
        #print pxarray
        print (xmax*ymax)
        print len(pxarray)
        
        pxmatrix = np.reshape(pxarray, (xmax, ymax, p))
        print pxmatrix.shape
        
        print "pixel check"
        pxerr = checkMatrixReshape(xmax, ymax, pxmatrix, pix)
        if not pxerr:
            sys.exit(1)
        print "AYOKAY!"
        
        print "RGB Check"
        rgberr = checkRGBVals(xmax, ymax, pxmatrix)
        if not rgberr:
            continue
        print "OKEYDOKE"
        
        print "Simplify Matrix RGB Vals"
        smplmatx = collapseMatrix(xmax, ymax, pxmatrix)
                
#        print smplmatx[20][20]
#        print pix[20,20]
        
        if (counter < 10):
            imgarr[counter+20] = smplmatx
        
        #outf.write("\nIMAGE MATRIX\n")
        #outf.write(' '.join(map(str, smplmatx)))
        
        counter+=1
    
    some_ID = 'O1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
        #cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'"%(some_ID))        
        # NEED single quotation marks around %s => '%s'
        # also "..."%(...) PERCENTsign NEEDEDor get typeerror http://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    #IDs with >=10 symbols: A1, Aa1, Aa13, D21, D36, D46, D58, G1, ...
        #G17, G43, I9, M17, M17x, N29, N35, N37, O1, O34, Q3, S29 ...
        #V1, V28, V31, W11, X1
    
    print "WHUT"
       
    #outf = open('L40Output.txt', 'w')       
    # the following works to load img from db into program for manip
    # https://docs.python.org/2/library/stringio.html
    # http://effbot.org/imagingbook/image.htm - see discussion under Image.fromstring
    counter = 0
    for GardID, Sys_Filename, Img in cursor:
        if (counter < 10):
            labelarr[counter+30] = GardID        
        
        (im, pix) = loadImg(cursor.fetchone()[2])
        print im.size
        (xmax, ymax) = im.size
        print im.size
#        print pix[30,23]
        
        if (im.mode == "RGB"):
            p = 3
        elif (im.mode == "RGBA"):
            p = 4
        
        pxarray = makePixelArray(xmax, ymax, pix)
        
        #print pxarray
        print (xmax*ymax)
        print len(pxarray)
        
        pxmatrix = np.reshape(pxarray, (xmax, ymax, p))
        print pxmatrix.shape
        
        print "pixel check"
        pxerr = checkMatrixReshape(xmax, ymax, pxmatrix, pix)
        if not pxerr:
            sys.exit(1)
        print "AYOKAY!"
        
        print "RGB Check"
        rgberr = checkRGBVals(xmax, ymax, pxmatrix)
        if not rgberr:
            continue
        print "OKEYDOKE"
        
        print "Simplify Matrix RGB Vals"
        smplmatx = collapseMatrix(xmax, ymax, pxmatrix)
                
#        print smplmatx[20][20]
#        print pix[20,20]
        
        if (counter < 10):
            imgarr[counter+30] = smplmatx
        
        #outf.write("\nIMAGE MATRIX\n")
        #outf.write(' '.join(map(str, smplmatx)))
        
        counter+=1
    
    
    outf2 = open('L40OutputFull.txt', 'w')
    outf2.write(' '.join(map(str, imgarr)))
    outf2.close
    
    print labelarr
    
                

    
    #for GardID, Sys_FileName, Img in cursor:
    #    print("GardID: {}, Sys_FileName: {}").format(GardID,Sys_FileName)
    #
    #print GardID
    #print Sys_FileName
        
    mariadb_connection.close()