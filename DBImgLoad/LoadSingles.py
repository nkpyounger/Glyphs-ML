# -*- coding: utf-8 -*-

# https://mariadb.com/blog/how-connect-python-programs-mariadb
# http://conda.pydata.org/docs/using/pkgs.html#install-a-package

# ^ all i needed - simple conda install, no external dl required

import MySQLdb as mariadb
from PIL import Image
import numpy as np
import StringIO

def mysqlLogin(filepath):
    myf = open(filepath, 'r')
    h = myf.readline()
    u = myf.readline()
    pw = myf.readline()
    
    h = h[:-1]
    u = u[:-1]
    pw = pw[:-1]
    
    return (h,u,pw)
    
    
if __name__ == '__main__':
    (h,u,pw) = mysqlLogin('C:\Users\USER\Documents\mysqlid.txt')
    
    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
    some_ID = 'A40'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
        # NEED single quotation marks around %s => '%s'
        # also "..."%(...) PERCENTsign NEEDEDor get typeerror http://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    print "WHUT"
       
       
    # the following works to load img from db into program for manip
    # https://docs.python.org/2/library/stringio.html
    # http://effbot.org/imagingbook/image.htm - see discussion under Image.fromstring
    for i in cursor:
        pic1 = cursor.fetchone()[2]
        output = StringIO.StringIO(pic1)
        im = Image.open(output)
        (xmax, ymax) = im.size
        pix = im.load()
        print im.size
        print pix[30,23]
        
        pxarray = []
    
        for i in range(xmax):
            for j in range(ymax):
                pxarray.append(list(pix[i,j])) 
        
        #print pxarray
        print (xmax*ymax)
        print len(pxarray)
        
        pxmatrix = np.reshape(pxarray, (xmax, ymax, 4))
        print pxmatrix.shape
        
        print "pixel check"
        for i in range(xmax):
            for j in range(ymax):
                if (np.array_equal(list(pix[i,j]),pxmatrix[i][j])):
                    #print "TRUE"
                    continue
                else:
                     print "ERROR"   
                     print list(pix[i,j])
                     print pxmatrix[i][j]
        print "AYOKAY!"
        
        print "RGB Check"
        for i in range(xmax):
            for j in range(ymax):
                if (pxmatrix[i][j][0] == pxmatrix[i][j][1] and pxmatrix[i][j][0] == pxmatrix[i][j][2]):
                    continue
                else:
                    print "error"
                    print pxmatrix[i][j]
                    print "at {}, {}".format(i,j)
        print "OKEYDOKE"
        
        print "Simplify Matrix RGB Vals"
        smplmatx = np.zeros((xmax,ymax), dtype=np.int)
#        print type(smplmatx[0][0])
        
#        print "OVERWRITE matrix of pixels"            
        for i in range(xmax):
            for j in range(ymax):
                smplmatx[i][j] = pxmatrix[i][j][0]
                
        print smplmatx[20][20]
        print pix[20,20]
                
        output.close()
    
    #for GardID, Sys_FileName, Img in cursor:
    #    print("GardID: {}, Sys_FileName: {}").format(GardID,Sys_FileName)
    #
    #print GardID
    #print Sys_FileName
        
    mariadb_connection.close()