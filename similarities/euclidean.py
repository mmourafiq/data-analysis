# -------------------------------------------------------------------------------
# Name:        Recommendations
# 
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from __future__ import division
from math import sqrt

EUCLIDEAN_SIMILARITY_CACHE = {}


def get_commun_items(x, y):
    """
    Returns the commun items between x and y
    """
    return [i for i in x.keys() if i in y.keys()]


def euclidean_dis(x, y, commun_items):
    """
    Returns the euclidean distance between x and y for a given list of commun items
    """
    return sqrt(sum([pow(x[i] - y[i], 2) for i in commun_items]))


def euclidean_sim(items, x, y, cache=False):
    """
    Returns the euclidean similarity between x and y.
    """
    if cache:
        if (x, y) in EUCLIDEAN_SIMILARITY_CACHE:
            return EUCLIDEAN_SIMILARITY_CACHE[(x, y)]
        i_x = items[x]
        i_y = items[y]
        sim = 1 / (1 + euclidean_dis(i_x, i_y, get_commun_items(i_x, i_y)))
        EUCLIDEAN_SIMILARITY_CACHE[(x, y)] = sim
        EUCLIDEAN_SIMILARITY_CACHE[(y, x)] = sim
        return sim
    i_x = items[x]
    i_y = items[y]
    return 1 / (1 + euclidean_dis(i_x, i_y, get_commun_items(i_x, i_y)))
