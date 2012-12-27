# -------------------------------------------------------------------------------
# Name:        map reduce class
#
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from __future__ import division
import collections
import itertools
import multiprocessing


class MapReduce(object):
    """
    The map reduce object, should be initialized with:
        map_fn
        reduce_fn
        nbr_workers
    """

    def __init__(self, map_fn, reduce_fn, num_workers=None):
        """
        initiaize the mapreduce object
            map_fn : Function to map inputs to intermediate data, takes as 
            input one arg and returns a tuple (key, value)
            reduce_fn : Function to reduce intermediate data to final result
            takes as arg keys as produced from the map, and the values associated with it
        """
        self.map_fn = map_fn
        self.reduce_fn = reduce_fn
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        """
        returns the mapped_values organised by their keys. (keys, associated values)
        """
        organised_data = collections.defaultdict(list)
        for key, value in mapped_values:
            organised_data[key].append(value)
        return organised_data.items()

    def __call__(self, inputs=None, chunk_size=1):
        """
        process the data through the map reduce functions.
        inputs : iterable
        chank_size : amount of data to hand to each worker 
        """
        mapped_data = self.pool.map(self.map_fn, inputs, chunksize=chunk_size)
        partioned_data = self.partition(itertools.chain(*mapped_data))
        reduced_data = self.pool.map(self.reduce_fn, partioned_data)
        return reduced_data
        
