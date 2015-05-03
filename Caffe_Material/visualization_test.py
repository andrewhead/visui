#! /usr/bin/env python

import numpy as np
import h5py as h5
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
CAFFE_ROOT = 'caffe'
import os.path
import sys
sys.path.insert(0, os.path.join(CAFFE_ROOT, 'python'))
import caffe

TEST_DIR = 'test'
LAYERS_FILE = os.path.join(CAFFE_ROOT, 'CS280_Homework2/question2_2_lenet.prototxt')
MODEL_FILE = os.path.join(CAFFE_ROOT, 'CS280_Homework2/snapshots/2_2_iter_10000.caffemodel')
HD5_SOURCE = os.path.join(TEST_DIR, 'h5source.txt')

# Plotting paramters inspired by http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/filter_visualization.ipynb
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


def vis_square(data, padsize=1, padval=0):
    ''' 
    Adapted from the Caffe visualization tutorial at
    http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/filter_visualization.ipynb. 
    It's supposed to visualize the filters.
    '''
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    data = data.reshape((data.shape[0], data.shape[1]))  # Lose the depth of the image for our grayscale depth-1 images
    
    print data.shape
    plt.imshow(data, cmap=cm.Greys_r)


def load_images():
    ''' Load all images from storage. '''
    image_list = []

    # Add images from all HDF5 files into one list
    with open(HD5_SOURCE) as hd5_source:
        for line in hd5_source.readlines():
            hd5_data = h5.File(line.strip(), 'r')
            for image in hd5_data['data']:
                image_list.append(image)

    images = np.array(image_list)
    return images


def main():
    ''' Main procedure to forward-propagate images through system and visualize the first layer. '''
    # Load caffe model
    net = caffe.Classifier(LAYERS_FILE, MODEL_FILE)

    # Run model on all test files to generate parameters at filters
    # I'm actually not positive that this step is at all necessary
    images = load_images()
    batch_size = net.blobs['data'].data.shape[0]
    for index in range(0, len(images), batch_size):
        batch_images = images[index:index+batch_size]
        net.blobs['data'].data[...] = batch_images
        out = net.forward()

    # Plot filters from first convolution layer
    filters = net.params['conv1'][0].data
    fig = plt.figure()
    vis_square(filters.transpose(0, 2, 3, 1))
    fig.savefig('filters.png')


if __name__ == '__main__':
    main()
