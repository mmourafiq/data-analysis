#-------------------------------------------------------------------------------
# Name:        graph analysis
#
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq 
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import collections
from math import exp

def bid_for_bider(bider, bids, item):
    """
    Returns the bid the bider put on item
    """
    return bids[item] if item in bids.keys() else 0

def fraction_for_bider(bider, remaining_budget, initial_budget, bids, item):
    """
    return the bid times 1 - e^-(fraction of remaining budget)
    """
    return bids[item]*(1 - exp(-(remaining_budget/initial_budget))) if item in bids.keys() else 0

def sort_biders(biders, bids=None, item=None, by_budget=False, by_bid=False, by_fraction=False):
    """
    sort biders by budget
    """
    result = []
    if by_budget and not by_bid:
        return sorted(biders, key=lambda x : x[1], reverse=True)
    if by_bid and item is not None and not by_budget:
        return sorted(biders, key=lambda (x,y,z) : bid_for_bider(x, bids[x], item), reverse=True)
    if by_fraction:
        return sorted(biders, key=lambda (x,y,z) : fraction_for_bider(x, y, z, bids[x], item), reverse=True)
    return biders

def greedy_adwords(biders, bids, items):
    """
    greedy algorithms make their decision in response to each input element by maximizing some
    function of the input element and the past.
    all click through rates are the same
    #bider structer : bider, remaining budget, initial budget
    #bids for bidder structer : item, value ...
    """
    result = []
    for item in items:
        biders = sort_biders(biders, bids, item=item, by_bid=True)
        for b in range(len(biders)):
            bider, remaining_budget, initial_budget = biders[b]
            if item in bids[bider].keys() and remaining_budget >= bids[bider][item]:
                result.append((item, bider))
                biders[b] = (bider, remaining_budget-bids[bider][item], initial_budget)
                break
    return result

def balance_adwords(biders, bids, items):
    """
    assigns a query to the advertiser who bids on the query and
    has the largest remaining budget. Ties may be broken arbitrarily.
    #bider structer : bider, remaining budget, initial budget
    #bids for bidder structer : item, value ...
    """
    result = []
    for item in items:
        biders = sort_biders(biders, by_budget=True)
        for b in range(len(biders)):
            bider, remaining_budget, initial_budget = biders[b]
            if item in bids[bider].keys() and remaining_budget >= bids[bider][item]:
                result.append((item, bider))
                biders[b] = (bider, remaining_budget-bids[bider][item], initial_budget)
                break
    return result

def generalized_balance_adwords(biders, bids, items):
    """
    differs from the balance algoritghms in two ways:
        bias the choice of the bider in favor of the one with the higher bid
        less absolute about the remaining budget, rather, consider the fraction of the remaining budget
    #bider structer : bider, remaining budget, initial budget
    #bids for bidder structer : item, value ...
    """
    result = []
    for item in items:
        biders = sort_biders(biders, bids, item=item, by_fraction=True)
        for b in range(len(biders)):
            bider, remaining_budget, initial_budget = biders[b]
            if item in bids[bider].keys() and remaining_budget >= bids[bider][item]:
                result.append((item, bider))
                biders[b] = (bider, remaining_budget-bids[bider][item], initial_budget)
                break
    return result


def test_greedy():
    biders = (("m",30, 30), ("l",10, 10), ("k",25, 25), ("p",20, 20))
    bids = {"m":{'a':2, 'b':3, 'd':1}, "l":{"c":1, 'a':5}, "p":{}, "k":{'b':5, 'c':2, 'd':1}}
    items = tuple(('a', 'b', 'd', 'a', 'a'))
    print greedy_adwords(biders=biders, bids=bids, items=items)

def test_balance():
    biders = (("m",30, 30), ("l",10, 10), ("k",25, 25), ("p",20, 20))
    bids = {"m":{'a':2, 'b':3, 'd':1}, "l":{"c":1, 'a':5}, "p":{}, "k":{'b':5, 'c':2, 'd':1}}
    items = tuple(('a', 'b', 'd', 'a', 'a'))
    print balance_adwords(biders=biders, bids=bids, items=items)

def test_ageneralized_balance():
    biders = (("m",30, 30), ("l",10, 10), ("k",25, 25), ("p",20, 20))
    bids = {"m":{'a':2, 'b':3, 'd':1}, "l":{"c":1, 'a':5}, "p":{}, "k":{'b':5, 'c':2, 'd':1}}
    items = tuple(('a', 'b', 'd', 'a', 'a'))
    print ageneralized_balance_adwords(biders=biders, bids=bids, items=items)

if __name__ == '__main__':
    test_greedy()
    test_balance()
    test_ageneralized_balance()
