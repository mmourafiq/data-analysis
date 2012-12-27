# -------------------------------------------------------------------------------
# Name:        cryptarithmetic
# 
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from __future__ import division


def inverse(f, delta=1 / 1024.):
    """
        given a function f, monotonically increasing on a positive interval
        return x = f_1(y) the approximation of its inverse function
    """

    def _f(y):
        lv, hv = find_bounds(f, y)
        return binary_search(f, y, lv, hv, delta)

    return _f


def find_bounds(f, y):
    """
        given a function f,
        return lv & hv such that lv <= t(y) <= hv
    """
    x = 1
    while f(x) < y:
        x = x * 2
    lv = 0 if x == 1 else x / 2
    return lv, x


def binary_search(f, y, lv, hv, delta):
    """
    recherche dicothomique.
    returns x such that f(x) is within delta of y : y-delta <= f(x) <= y+delta
    for exact approximation delta should be as small as possible
    """
    while lv <= hv:
        x = (lv + hv) / 2
        if f(x) > y:
            hv = x - delta
        elif f(x) < y:
            lv = x + delta
        else:
            return x
    return hv if f(hv) - y < y - f(lv) else lv


def square(x): return x * x


def power4(x): return x ** 4


sqrty = inverse(square)
log4 = inverse(power4)
print square(3)
print power4(3)
print sqrty(9)
print log4(81)
    
