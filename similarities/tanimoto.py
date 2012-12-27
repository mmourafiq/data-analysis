'''
Created on Aug 22, 2012

@author: mourad mourafiq
'''

TANIMOTO_SIMILARITY_CACHE = {}


def tanimoto_sim(items, x, y, cache=False):
    """
    Returns the similarity between x and y based on the tanimoto score
    """
    c1, c2, shr = 0, 0, 0

    for i in range(len(x)):
        if x[i] != 0: c1 += 1  # in v1
        if y[i] != 0: c2 += 1  # in v2
        if x[i] != 0 and y[i] != 0: shr += 1  # in both

    return 1.0 - (float(shr) / (c1 + c2 - shr))
