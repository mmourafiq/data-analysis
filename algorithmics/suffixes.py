from __future__ import division


def check_in(i_from, i_to, str, sfx):
    sum = 0
    for i in range(i_from, min(i_to, len(sfx))):
        if sfx[i] == str[i]:
            sum += 1
        else:
            break
    return sum


def suffix():
    N = int(raw_input())
    for i in range(N):
        sum = 0
        str = raw_input()
        len_str = len(str)
        sum += len_str
        sfx = str[1:]
        cpt = 2
        while sfx != "":
            len_sfx = len(sfx)
            step = 90
            for i in range(0, len_sfx, step):
                if str[i:i + step] == sfx[i:i + step]:
                    sum += step
                else:
                    sum += check_in(i, i + step, str, sfx)
                    break
            sfx = str[cpt:]
            cpt += 1
        print sum


import time

t = time.clock()
suffix()
print time.clock() - t          
