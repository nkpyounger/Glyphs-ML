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

if __name__ == '__main__':
    
    imgarr = [None]*40
    labelarr = [None]*40
      
    
    (h,u,pw) = mysqlLogin('C:\Users\USER\Documents\mysqlid.txt')
    
    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("SELECT GardID,Src,Sys_FileName,Img FROM sign_list")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    MaxIDX = ""
    MaxIDY = ""
    MaxSrcX = ""
    MaxSrcY = ""
    MaxFileNameX = ""
    MaxFileNameY = ""
    MaxX = 0
    MaxY = 0
    MaxImModeX = ""
    MaxImModeY = ""
    print "({}, {})".format(MaxX, MaxY)
        
    for GardID, Src, Sys_Filename, Img in cursor:
        (im, pix) = loadImg(cursor.fetchone()[3])
        (xdim, ydim) = im.size
        
        if (xdim > MaxX):
            MaxX = xdim
            MaxIDX = GardID
            MaxSrcX = Src
            MaxFileNameX = Sys_Filename
            MaxImModeX = im.mode
            print "({}, {})".format(MaxX, MaxY)
            
        if (ydim > MaxY):
            MaxY = ydim
            MaxIDY = GardID
            MaxSrcY = Src
            MaxFileNameY = Sys_Filename
            MaxImModeY = im.mode
            print "({}, {})".format(MaxX, MaxY)
            
        
    print "({}, {})".format(MaxX, MaxY)
    print "({}, {})".format(MaxIDX, MaxIDY)
    print "({}, {})".format(MaxSrcX, MaxSrcY)
    print "({}, {})".format(MaxFileNameX, MaxFileNameY)
    print "({}, {})".format(MaxImModeX, MaxImModeY)
        
            
        
        
    mariadb_connection.close()