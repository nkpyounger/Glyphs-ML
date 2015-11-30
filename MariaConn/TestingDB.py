# -*- coding: utf-8 -*-

import MySQLdb as mariadb

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
    
#    count = [None]*40
#    labels = [None]*40
#    padarr = [None]*40
      
    
    (h,u,pw) = mysqlLogin('/home/nyounger/Documents/mysqlid.txt')
    
    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
#    some_ID = 'A1'
#    some_src = 'EG-W'
    try:
        cursor.execute("SELECT GardID FROM sign_list")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    lblcount = 0
    prevID = ''
    labels = []
    
    for GardID in cursor:
#        if any(prevID in s for s in labels):
        if (GardID in labels):
#            print '{}, {}'.format(prevID, GardID)
            continue
        else:
            prevID = GardID
            labels.append(GardID)
            lblcount += 1
    
#    labels = [None] * lblcount
    
#    cursor = mariadb_connection.cursor()
#    some_src = 'EG-W'
#    try:
#        cursor.execute("SELECT GardID FROM sign_list")
#    except mariadb.Error as error:
#        print("Error: {}".format(error))
#        
#    i = 0
#    prevID = None
#    for GardID in cursor:
#        if (prevID == GardID):
#            continue
#        else:
#            prevID = GardID
#            labels[i] = GardID
#            i += 1
        
    print labels
#    prevID = GardID
#    print 'testing'
#    matching = [s for s in labels if 'Aa1' in s]
#    print matching
#    print prevID
#    print prevID in labels
#    print type(prevID)
#    print type(str(prevID))
#    print str(prevID)
#    prevID = str(prevID)[1:-2]
#    print prevID
#    print type(prevID)
#    print 'iunno'
#    if any(prevID in s for s in labels):
#        print s
#        
#    print 'v2'
#    matching = [s for s in labels if prevID in s]
#    print matching
#    
#    print [el for el in labels if prevID in el]
##        print el
##    else:
##        print 'noooooo'
#    print prevID in labels
    
#    mariadb_connection.close()
    
    itemcount = [None] * lblcount
#    mariadb_connection = mariadb.connect(host=h, user=u, passwd=pw, db='glyphscopy_testing')
    cursor = mariadb_connection.cursor()
    some_src = 'EG-W'
    for i in range(lblcount):
        icount = 0
        some_ID = str(labels[i])[2:-3]
#        print some_ID
#        some_ID = labels[i]
#        print "SELECT Sys_FileName FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src)
        try:
            cursor.execute("SELECT Sys_FileName FROM sign_list WHERE GardID='%s'AND Src='%s'"%(some_ID, some_src))
        except mariadb.Error as error:
            print("Error: {}".format(error))
        for Sys_FileName in cursor:
            icount += 1
        itemcount[i] = icount
        
    print itemcount
    
    for i in range(lblcount):
        print "{}, {}".format(labels[i], itemcount[i])
        
    print "40 or Greater"
    for i in range(lblcount):
        if itemcount[i] > 39:
            print "{}, {}".format(labels[i], itemcount[i])
        
    
    mariadb_connection.close()   
    