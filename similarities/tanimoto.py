'''
Created on Aug 22, 2012

@author: pipado
'''

TANIMOTO_SIMILARITY_CACHE = {}


def get_commun_items(x, y):
    """
    Returns the commun items between x and y
    """
    return [i for i in x.keys() if i in y.keys()] 


def tanimoto_score(x, y, commun_items):
    """
    Return the tanimoto score :
        X inter Y / X union Y
    """
    return len(commun_items)/(len(x) + len(y))

def tanimoto_sim(items, x, y, cache=False):
    """
    Returns the similarity between x and y based on the tanimoto score
    """
    if cache:
        if (x,y) in TANIMOTO_SIMILARITY_CACHE:
            return TANIMOTO_SIMILARITY_CACHE[(x,y)]
        i_x = items[x]
        i_y = items[y]
        sim = tanimoto_score(i_x, i_y, get_commun_items(i_x, i_y))
        TANIMOTO_SIMILARITY_CACHE[(x,y)] = sim
        TANIMOTO_SIMILARITY_CACHE[(y,x)] = sim
        return sim
    i_x = items[x]
    i_y = items[y]
    return tanimoto_score(i_x, i_y, get_commun_items(i_x, i_y))