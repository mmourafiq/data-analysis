# -------------------------------------------------------------------------------
# Name:        estimation of pi with map reduce
#
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from __future__ import division
import multiprocessing
import numpy
import random
from map_reduce import MapReduce

NBR_POINTS = 1000000
RADIUQ = numpy.sqrt(NBR_POINTS)
NBR_WORKERS = 4
NBR_PER_WORKER = NBR_POINTS / NBR_WORKERS


def probability_calculation(item):
    """Read a file and return a sequence of (word, occurances) values.
    """

    print multiprocessing.current_process().name, 'calculating', item
    output = []
    IN_CIRCLE = 0
    for i in range(int(NBR_PER_WORKER)):
        x = numpy.random.randint(0, RADIUQ)
        y = numpy.random.randint(0, RADIUQ)
        if (numpy.sqrt(x ** 2 + y ** 2) < RADIUQ):
            IN_CIRCLE += 1
    output.append(('pi', IN_CIRCLE))
    return output


def estimate_pi(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    key, occurances = item
    return (sum(occurances) / NBR_POINTS) * 4


if __name__ == '__main__':
    mapper = MapReduce(probability_calculation, estimate_pi)
    pi = mapper([i for i in range(NBR_WORKERS)])
    print pi
