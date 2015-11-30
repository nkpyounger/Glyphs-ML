# -*- coding: utf-8 -*-

import MySQLdb as mariadb
from PIL import Image
import numpy as np
import StringIO
import sys
from matplotlib import pyplot
import TrainTestSets2 as tts #dash in name produces 'invalid syntax'
import SetPadding as pad

from random import shuffle

def padImages(img_matx, offset, rsize, csize):
    z_arr = np.zeros((rsize, csize), dtype = np.int)
    z_arr[:][:] = 255 #white bkgd
#    print z_arr.shape
    (rows, cols) = img_matx.shape
#    print "rows = {}, cols = {}".format(rows,cols)
    
    if (rows % 2): #if odd
        rtemp = rows + 1
    else:
        rtemp = rows
        
    if (cols % 2):
        ctemp = cols + 1
    else:
        ctemp = cols
        
#    xtemp = xtemp / 2
#    ytemp = ytemp / 2
    
    c_start = (csize / 2) - (ctemp / 2)
    r_start = (rsize / 2) - (rtemp / 2)
#    print "c = {}, r = {}".format(c_start, r_start)
    
    for i in range(rows):
        for j in range(cols):
#            print "i = y = row = {}, j = x = col = {}".format(i,j)
            z_arr[r_start + i][c_start + j] = img_matx[i][j]
            
#    pad_array[offset] = z_arr
#    return pad_array
    return z_arr
    
####
class NearestNeighborClassifier(object):
    """A generic k-nearest neighbor predictor.

    You need to extend this class and implement distance(from, to)
    and consensus(label_list) in order to make this functional."""
    
    def __init__(self, dataset, k):
        """Create a new nearest neighbor classifier.

        dataset - a list of data points. Each data point is an (x, y) pair,
                  where x is the input and y is the label.
        k - the number of neighbors to search for."""
        # Note how we don't have to do any initialization!
        # Once we have a dataset, we can immediately get predictions on new values.
        self.dataset = dataset
        self.k = k
        
    def predict(self, point):
        # We have to copy the data set list, because once we've located the best
        # candidate from it, we don't want to see that candidate again, so we'll delete it.
        candidates = self.dataset[:]
        
        # Loop until we've gotten all the neighbors we want.
        neighbors = []
        while len(neighbors) < self.k:
            # Compute distances to every candidate.
            distances = [self.distance(x[0], point) for x in candidates]
#            print distances
            
            # Find the minimum distance neighbor.
            best_distance = min(distances)
            index = distances.index(best_distance)
            neighbors.append(candidates[index])
            
            # Remove the neighbor from the candidates list.
            del candidates[index]
        
        # Predict by averaging the closets k elements.
        prediction = self.consensus([value[1] for value in neighbors])
        return prediction
    
def euclidean_distance(img1, img2):
    # Since we're using NumPy arrays, all our operations are automatically vectorized.
    # A breakdown of this expression:
    #     img1 - img2 is the pixel-wise difference between the images
    #     (img1 - img2) ** 2 is the same thing, with each value squared
    #     sum((img1 - img2) ** 2) is the sum of the elements in the matrix.
#    return sum((img1 - img2) ** 2) ##IMAGES MUST HAVE SAME DIMENSIONS :
    return sum(sum((img1 - img2) ** 2))#WHYYYYYYYY
    
from collections import defaultdict
def get_majority(votes):
    # For convenience, we're going to use a defaultdict.
    # This is just a dictionary where values are initialized to zero
    # if they don't exist.
    counter = defaultdict(int)
    for vote in votes:
        # If this weren't a defaultdict, this would error on new vote values.
        counter[vote] += 1
        
    # Find out who was the majority.
    majority_count = max(counter.values())
    for key, value in counter.items():
        if value == majority_count:
            return key

class MNISTPredictor(NearestNeighborClassifier):
    def distance(self, p1, p2):
        return euclidean_distance(p1, p2)
    
    def consensus(self, values):
        return get_majority(values)
        
def predict_test_set(predictor, test_set):
    """Compute the prediction for every element of the test set."""
    predictions = [predictor.predict(test_set[i]) for i in xrange(len(test_set))]
    return predictions
    
def evaluate_prediction(predictions, answers):
    """Compute how many were identical in the answers and predictions,
    and divide this by the number of predictions to get a percentage."""
    correct = sum(np.asarray(predictions) == np.asarray(answers))
    total = float(np.prod(answers.shape))
    return correct / total

if __name__ == '__main__':
    (trainlbl, trainimg, testlbl, testimg) = tts.BuildArrays()
#    print trainlbl
    (ysize, xsize) = pad.SetPaddingSize(trainlbl, trainimg, testlbl, testimg)
    #note above (TO FIX) your ability to confuse x and y...
#    print xsize, ysize
    
    trainpad = [None] * len(trainimg)
    testpad = [None] * len(testimg)
    
#    print len(trainpad)
#    print len(testpad)

    for i in range(len(trainpad)):
        trainpad[i] = padImages(trainimg[i], i, ysize, xsize)
        print "Success #{}".format((i+1))    
        
    for i in range(len(testpad)):
        testpad[i] = padImages(testimg[i], i, ysize, xsize)
        print "Success #{}".format((i+1))
        
#    #Visualization of random elements
#    # Get the figure and axes.
#    fig, axes = pyplot.subplots(5, 5)
#    axes = axes.reshape(25)
#    fig.suptitle("Random Sampling of Glyphs")
#    
#    # Plot random images.
#    indices = np.random.randint(len(trainpad), size=25)
#    for axis, index in zip(axes, indices):
#        image = trainpad[index]#[index, :, :]
#        axis.get_xaxis().set_visible(False)
#        axis.get_yaxis().set_visible(False)
#        axis.imshow(image, cmap = pyplot.cm.Greys_r)
        
 # Convert our data set into an easy format to use.
    # This is a list of (x, y) pairs. x is an image, y is a label.
    dataset = []
    for i in xrange(len(trainpad)):
        dataset.append((trainpad[i], trainlbl[i]))
        
    outf3 = open('kNNDiffSetsDataset.txt', 'w')
    outf3.write(' '.join(map(str, dataset)))
    outf3.close
    
    
    ks = [1, 2, 3, 4, 5, 6]
    predictors = [MNISTPredictor(dataset, k) for k in ks] #instantiate 6 nearestneighbor classes
    #predictors doesn't showin variable list
#    #set predictor
#    k = 1
#    
#    predictor = MNISTPredictor(dataset, k)
#    ###thus far doesn't throw up any errors
    
    # Choose a subset of the test set. Otherwise this will never finish.
    test_set = testpad
#    pred = predict_test_set(predictor, test_set)
    all_predictions = [predict_test_set(predictor, test_set) for predictor in predictors]
    
    labels = np.asarray(testlbl) #100%accurate
#    labels[15] = 'Aa1' #to trick classifier
#    shuffle(labels)    #reduces to ~25% accurate - what would be expected
    
#    accuracies = evaluate_prediction(pred, labelarr)
    accuracies = [evaluate_prediction(pred, labels) for pred in all_predictions]
#    print accuracies
    
    # Draw the figure.
    fig = pyplot.figure(1)
#    pyplot.plot(k, accuracies, 'ro', figure=fig)
#    fig = figure(1)
    pyplot.plot(ks, accuracies, 'ro', figure=fig)
    
#    fig.suptitle("Nearest Neighbor Classifier Accuracies")
#    fig.axes[0].set_xlabel("k (# of neighbors considered)")
#    fig.axes[0].set_ylabel("accuracy (% correct)");
#    fig.axes[0].axis([0, max(k) + 1, 0, 1]);
    
    fig.suptitle("Nearest Neighbor Classifier Accuracies")
    fig.axes[0].set_xlabel("k (# of neighbors considered)")
    fig.axes[0].set_ylabel("accuracy (% correct)");
    fig.axes[0].axis([0, max(ks) + 1, 0, 1]);
    
