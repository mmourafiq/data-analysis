# -------------------------------------------------------------------------------
# Name:        decorators
# 
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from functools import update_wrapper
import time


def decorator(d):
    "Make function d a decorator: d wraps a function fn."

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def trace(f):
    """
    helps debug recursive calls
    """
    indent = '   '

    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level * indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level - 1) * indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result

    trace.level = 0
    return _f


@decorator
def timing(f):
    """
    calculates time of computation
    """
    def _f(*args):
        t0 = time.clock()
        result = f(*args)
        print t0
        t =  time.clock()
        print t
        return result
    return _f

@decorator
def memo(f):
    """
    a simple caching decorator
    """
    cache = {}

    def _f(*args):
        try :
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return f(args)
    return _f


@decorator
def count_calls(f):
    """
    counts the number of calls to the function f
    """
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

callcounts = {}
