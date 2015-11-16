# -*- coding: utf-8 -*-

# https://mariadb.com/blog/how-connect-python-programs-mariadb
# http://conda.pydata.org/docs/using/pkgs.html#install-a-package

# ^ all i needed - simple conda install, no external dl required

import MySQLdb as mariadb

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
    
pic1 = cursor.fetchone()[2]

for GardID, Sys_FileName, Img in cursor:
    print("GardID: {}, Sys_FileName: {}").format(GardID,Sys_FileName)

print GardID
print Sys_FileName
    
mariadb_connection.close()