import collections


def reduce_str(strg):
    count_abc = collections.defaultdict(int)
    str_g = list(strg)
    for s in str_g:
        count_abc[s] += 1
    if (count_abc['a'] == 0 and count_abc['c'] == 0) or (count_abc['a'] == 0 and count_abc['b'] == 0) or (
                    count_abc['b'] == 0 and count_abc['c'] == 0):
        return len(strg)
    elif (count_abc['a'] % 2 == count_abc['b'] % 2 == count_abc['c'] % 2):
        return 2
    else:
        return 1


def string_red():
    T = int(raw_input())
    r = set()
    for t in xrange(T):
        case = raw_input()
        print reduce_str(case)


string_red()
        
