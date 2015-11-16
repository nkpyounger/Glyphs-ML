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