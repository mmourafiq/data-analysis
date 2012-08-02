#-------------------------------------------------------------------------------
# Name:        shingling minhashing
# 
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from __future__ import division
from itertools import combinations

#exemple of baskets
BASKETS =(
set(('cat', 'and', 'dog', 'bites')),
set(('yahoo', 'news', 'claims', 'a', 'cat', 'mated', 'with', 'dog', 'and', 'produced', 'viable', 'offspring')),
set(('cat', 'killer', 'is', 'a', 'free', 'big', 'dog')),
set(('professional', 'free', 'advice', 'on', 'dog', 'training', 'puppy', 'training')),
set(('cat', 'and','kitten', 'training', 'behavior')),
set(('dog',  'cat', 'provides', 'training', 'in', 'eugene', 'oregon')),
set(('dog', 'cat', 'is', 'slang', 'term', 'used', 'by', 'police', 'officers', 'for', 'malefemale', 'relationship')),
set(('shop', 'for', 'your', 'show', 'dog', 'grooming', 'and', 'yet', 'pet', 'supplier'))
)

def frequency(baskets, item):
    """
    Frequency of item in baskets
    """
    freq = 0
    for basket in baskets:
        if item <= basket : freq += 1
    return freq

def frequent(frequency, support):
    """
    If frequency of item is bigger than support then it is ferquent
    """
    return True if frequency > support else False

def confidence(baskets, item1, item2):
    """
    Confidence of the rule Item1 -> item2 is the ratio freq2/freq1
    """
    item = item1 | item2
    freq1 = frequency(baskets=baskets, item=item1)
    freq2 = frequency(baskets=baskets, item=item)
    print freq1
    print freq2
    return freq2/freq1 if freq1>0 else 0

def interest(baskets, item1, item2):
    """
    the interest of an association rule item1->item2 to be the difference
    between its confidence and the fraction of baskets that contain item2.
    """
    return confidence(baskets=baskets, item1=item1, item2=item2) - (frequency(baskets=baskets, item=item2) / len(baskets))

def ferquent_items(baskets, support):
    """
    Determines which items are frequent
    """
     #items in baskets
    items = set()
    for basket in baskets:
        items |= basket
    pos = 0
    #first we determine which items are ferquent
    items_frequency = {}
    for item in items:
        freq = frequency(baskets, set([item]))
        items_frequency[item] = (freq, frequent(freq, support))
    return [(item, i_frequency) for item, (i_frequency, i_frequent) in items_frequency.items() if i_frequent]

def frequent_pairs(baskets, support):
    """
    Determines which pairs are frequent
    A-priori algorithm
    """
    frequent_items = [item for item, i_frequency in ferquent_items(baskets, support)]
    pairs_frequency = {}
    for pair in combinations(frequent_items, 2):
        if pair not in pairs_frequency:
            freq = frequency(baskets, set(pair))
            pairs_frequency[pair] = (freq, frequent(freq, support))
    print pairs_frequency

def son_algo(baskets, support, fraction_baskets):
    """
        the algorithm of savasere, omniescinski and navathe
        divide the input into nbr fractions, for each fraction find all frequent
        items for (1/fraction_baskets)*support
    """
    items = set()
    nbr_baskets = len(baskets)
    for i in range(0, nbr_baskets, fraction_baskets):
        items |= set(ferquent_items((baskets[i:i+3]), (fraction_baskets/nbr_baskets) * support))
    return [item for item, i_frequency in ferquent_items(baskets, support) if i_frequency > support]
