#-------------------------------------------------------------------------------
# Name:        jaccard similarity
# 
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from __future__ import division

EX_TUP_1 = ('a','a','a','b')
EX_TUP_1 = ('a','a','b','b','c')

def jaccard_sim(tup_1, tup_2, verbose=False):
    """
        calculate the jaccard similiarity of 2 tuples
    """
    sum = len(tup_1) + len(tup_2)
    set_1 = set(tup_1)
    set_2 = set(tup_2)
    inter = 0
    for i in (set_1 & set_2):
        count_1 = tup_1.count(i)
        count_2 = tup_2.count(i)
        inter += count_1 if count_1 < count_2 else count_2
    j_sim = inter/sum
    if verbose : print j_sim
    return j_sim

def jaccard_distance(tup_1, tup_2):
    """
        Calculate the jaccard distance
    """
    return 1 - jaccard_sim(tup_1, tup_2)

def jaccard_conditional_comparaison(tup, list_tups, min_jaccard_sim, verbose=False):
    """
        Suppose that "s" is a string of length "ls", and we are looking for
        strings with at least "sim" Jaccard similarity.
        To be sure that we do not have to compare "s" with "t", we must be certain that "sim" > ("ls" ? "p")/"ls". That
        is, "p" must be at least [(1 ? "sim")"ls"] + 1. Of course we want "p" to be as small as
        possible, so we do not index string s in more buckets than we need to. Thus,
        we shall hereafter take "p" = [(1 ? "sim")"ls"+ 1 to be the length of the prefix that
        gets indexed.
         P.S : "p" being the prefix of potential strings to be compared to "s"
         Case 1: p ? q. Here, the maximum size of the intersection is
            Ls ? i + 1 ? (p ? q)
            Since Ls = i + p, we can write the above expression for the intersection size as
            q + 1. The minimum size of the union is Ls + j ? 1, as it was when we did not
            take suffix length into account. Thus, we require
            (q + 1) /(Ls + j ? 1) ? J whenever p ? q.
         Case 2: p < q. Here, the maximum size of the intersection is Ls ? i + 1, as
            when suffix length was not considered. However, the minimum size of the union
            is now Ls + j ? 1 + q ? p. If we again use the relationship Ls = i + p, we can
            replace Ls ? p by i and get the formula i + j ? 1 + q for the size of the union.
            If the Jaccard similarity is at least J, then
            (Ls ? i + 1) / (i + j ? 1 + q) ? J
            whenever p < q.

    """
    tup_length = len(tup)
    pre = int(((1 - min_jaccard_sim) * tup_length) + 1)
    max_length = int(tup_length/min_jaccard_sim)
    min_length = tup_length - pre
    potential_tups = []
    for t in list_tups:
        t_length = len(t)
        #first we check teh current tup length
        if t_length >= min_length and t_length <= max_length:
            #second we should loop over all possible values for i & j
            for i in range(0, pre):
                for j in range(0, pre):
                    p = tup_length - i
                    q = t_length -j
                    if (p >= q and ((q + 1)/(tup_length + j -1)) >= min_jaccard_sim) or (p < q and ((tup_length - i + 1) / (i + j -1 + q)) >= min_jaccard_sim):
                        potential_tups.append(t)
    if verbose: print potential_tups
    return potential_tups
