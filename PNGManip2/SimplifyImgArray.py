from PIL import Image
import numpy as np

if __name__ == '__main__':
    im = Image.open("Wb01-Vorwort-A-1501.png") #Can be many different formats.
    pix = im.load()
    print im.size #Get the width and hight of the image for iterating over
    print pix[19,17] #Get the RGBA Value of the a pixel of an image
    #pix[x,y] = value # Set the RGBA Value of the image (tuple)
    print type(pix[55,25])
    
    
    (xmax, ymax) = im.size
    print xmax
    print ymax
    
#    pxarray = np.zeros((xmax, ymax))
    pxarray = []
    
    for i in range(xmax):
        for j in range(ymax):
            pxarray.append(list(pix[i,j]))
            
    print pxarray
    print len(pxarray)
    
    pxmatrix = np.reshape(pxarray, (xmax, ymax, 4))
    # see later checking - this works
    
    print pxmatrix
    
    print pxmatrix.shape
    print pxarray[0]
    
    print "pixel check"
    print pxarray[467]
    print pix[19,17]
    print pxmatrix[19][17]
    
    for i in range(xmax):
        for j in range(ymax):
            if (np.array_equal(list(pix[i,j]),pxmatrix[i][j])):
                #print "TRUE"
                continue
            else:
                 print "ERROR"   
                 print list(pix[i,j])
                 print pxmatrix[i][j]
                 
    for i in range(xmax):
        for j in range(ymax):
            if (pxmatrix[i][j][0] == pxmatrix[i][j][1] and pxmatrix[i][j][0] == pxmatrix[i][j][2]):
                continue
            else:
                print "error"
                print pxmatrix[i][j]
                print "at {}, {}".format(i,j)
                
    smplmatx = np.zeros((xmax,ymax), dtype=np.int)
    print type(smplmatx[0][0])
    
    print "OVERWRITE matrix of pixels"            
    for i in range(xmax):
        for j in range(ymax):
            smplmatx[i][j] = pxmatrix[i][j][0]
            #print pxmatrix[i][j]
            
    print "WHUT"
    print smplmatx
    print np.shape(smplmatx)
    print pix[19,17][0]
    print smplmatx[19][17]
    print type(smplmatx[19][17])
    
#    for i in range(xmax):
#        for j in range(ymax):
#            if (pxmatrix[i][j] == pix[i,j])
                
#ALL RGB Vals are same