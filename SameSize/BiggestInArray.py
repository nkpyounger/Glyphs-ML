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

if __name__ == '__main__':
    
    imgarr = [None]*40
    labelarr = [None]*40
    
    (h,u,pw) = mysqlLogin('C:\Users\USER\Documents\mysqlid.txt')

    print h
    print u
    print pw
    
    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
    some_ID = 'A1'
    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
    except mariadb.Error as error:
        print("Error: {}".format(error))
