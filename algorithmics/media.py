from __future__ import division


def add(e, min_s, max_s, max_min, min_max, l_min, l_max):
    if l_min == 0:
        min_s.append(e)
        max_min = e
        l_min += 1
        return True, max_min, min_max, l_min, l_max
    if e <= max_min:
        l_min += 1
        min_s.append(e)
    else:
        if e < min_max or l_max == 0:
            min_max = e
        l_max += 1
        max_s.append(e)
    return True, max_min, min_max, l_min, l_max


def remove(e, min_s, max_s, max_min, min_max, l_min, l_max):
    if e in min_s:
        l_min -= 1
        min_s.remove(e)
        if e == max_min:
            if l_min > 0:
                max_min = max(min_s)
            else:
                max_min = 0
        return True, max_min, min_max, l_min, l_max
    if e in max_s:
        l_max -= 1
        max_s.remove(e)
        if e == min_max:
            if l_max > 0:
                min_max = min(max_s)
            else:
                min_max = 0
        return True, max_min, min_max, l_min, l_max
    return True, max_min, min_max, l_min, l_max


def operate(op, e, min_s, max_s, max_min, min_max, l_min, l_max):
    if op == "a": return add(e, min_s, max_s, max_min, min_max, l_min, l_max)
    if op == "r": return remove(e, min_s, max_s, max_min, min_max, l_min, l_max)
    return False, max_min, min_max, l_min, l_max


def size_s(min_s, max_s, max_min, min_max, l_min, l_max):
    if l_min == l_max == 0:
        return False, max_min, min_max, l_min, l_max
    if l_max > l_min:
        e = min_max
        max_s.remove(e)
        l_max -= 1
        if l_max > 0:
            min_max = min(max_s)
        else:
            min_max = 0
        min_s.append(e)
        l_min += 1
        max_min = e
        return True, max_min, min_max, l_min, l_max
    if l_min > l_max + 1:
        e = max_min
        min_s.remove(e)
        l_min -= 1
        if l_min > 0:
            max_min = max(min_s)
        else:
            max_min = 0
        max_s.append(e)
        l_max += 1
        min_max = e
        return True, max_min, min_max, l_min, l_max
    return True, max_min, min_max, l_min, l_max


def calculate(min_s, max_s, max_min, min_max, l_min, l_max):
    if l_min > l_max:
        print max_min
    if l_min == l_max:
        med = max_min + min_max
        if med % 2 == 0:
            print "%.0lf" % (med / 2)
        else:
            print "%.1lf" % (med / 2)


def median():
    n_op = int(raw_input())
    min_s = []
    max_min = 0
    l_min = 0
    max_s = []
    min_max = 0
    l_max = 0
    for i in xrange(n_op):
        op, e = [x for x in raw_input().split()]
        e = int(e)
        stat, max_min, min_max, l_min, l_max = operate(op, e, min_s, max_s, max_min, min_max, l_min, l_max)
        if stat:
            stat, max_min, min_max, l_min, l_max = size_s(min_s, max_s, max_min, min_max, l_min, l_max)
            if stat:
                calculate(min_s, max_s, max_min, min_max, l_min, l_max)
            else:
                print "Wrong!"
        else:
            print "Wrong!"


median()
