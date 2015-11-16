# -*- coding: utf-8 -*-

# https://mariadb.com/blog/how-connect-python-programs-mariadb
# http://conda.pydata.org/docs/using/pkgs.html#install-a-package

# ^ all i needed - simple conda install, no external dl required

import MySQLdb as mariadb
from PIL import Image
import numpy as np
import StringIO



myf = open('C:\Users\USER\Documents\mysqlid.txt', 'r')
h = myf.readline()
u = myf.readline()
pw = myf.readline()

h = h[:-1]
u = u[:-1]
pw = pw[:-1]
    

    
    
mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
cursor = mariadb_connection.cursor()
some_name = 'A40'
try:
    cursor.execute("SELECT GardID,Sys_FileName,Img FROM sign_list WHERE GardID='%s'"%(some_name))
    # NEED single quotation marks around %s => '%s'
    # also "..."%(...) PERCENTsign NEEDEDor get typeerror http://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
except mariadb.Error as error:
    print("Error: {}".format(error))
    
print "WHUT"
   
   
# the following works to load img from db into program for manip
# https://docs.python.org/2/library/stringio.html
# http://effbot.org/imagingbook/image.htm - see discussion under Image.fromstring
pic1 = cursor.fetchone()[2]
output = StringIO.StringIO(pic1)
im = Image.open(output)
pix = im.load()
print im.size
print pix[30,23]
output.close()

for GardID, Sys_FileName, Img in cursor:
    print("GardID: {}, Sys_FileName: {}").format(GardID,Sys_FileName)

print GardID
print Sys_FileName
    
mariadb_connection.close()