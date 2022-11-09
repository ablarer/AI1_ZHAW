# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:28:50 2016

@author: stdm
"""

from sklearn.datasets import fetch_lfw_people
import numpy
   
class DataSet(object):
    def __init__(self, images):
        self._num_examples = images.shape[0]
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
        images = numpy.multiply(images, 1.0 / 255.0)
        self._images = images
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images
    
    @property
    def num_examples(self):
        return self._num_examples
  
    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._images = self._images[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], None

def read_data_sets():
    class DataSets(object):
        pass
    data_sets = DataSets()
    
    #LFW has 250x250 pixels, MNIST has 28x28
    print ("fetching data...")
    lfw_people = fetch_lfw_people(slice_=(slice(70, 195, None), slice(70, 195, None)), resize=0.224) 
    print ("done.")
    n_images, n_pixels = lfw_people.data.shape
    print("n_images: %d" % n_images)
    print("n_pixels: %d" % n_pixels)

    data_sets.train = DataSet(lfw_people.data)
    return data_sets