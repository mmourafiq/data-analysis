# circle sum
import sys

sys.setrecursionlimit(15000)


def cal_sum():
    T = int(raw_input())

    def c_sum(a, indice, start, end, N, round, a_cache):
        c = a[indice]
        if round == 0: return c
        if (indice, round) in a_cache:
            c = a_cache[(indice, round)]
        else:
            i_l = (indice - 1) % N
            i = indice
            i_r = (indice + 1) % N
            if round == 1:
                if i == start:
                    c = a[i_l] + a[i] + a[i_r]
                elif i == end:
                    c = c_sum(a, i_l, start, end, N, round, a_cache) + a[i] + c_sum(a, i_r, start, end, N, round,
                                                                                    a_cache)
                else:
                    c = c_sum(a, i_l, start, end, N, round, a_cache) + a[i] + a[i_r]
            else:
                if i == start:
                    c = c_sum(a, i_l, start, end, N, round - 1, a_cache) + c_sum(a, i, start, end, N, round - 1,
                                                                                 a_cache) + c_sum(a, i_r, start, end, N,
                                                                                                  round - 1, a_cache)
                elif i == end:
                    c = c_sum(a, i_l, start, end, N, round, a_cache) + c_sum(a, i, start, end, N, round - 1,
                                                                             a_cache) + c_sum(a, i_r, start, end, N,
                                                                                              round, a_cache)
                else:
                    c = c_sum(a, i_l, start, end, N, round, a_cache) + c_sum(a, i, start, end, N, round - 1,
                                                                             a_cache) + c_sum(a, i_r, start, end, N,
                                                                                              round - 1, a_cache)
            a_cache[(indice, round)] = c % 1000000007
        return c

    for t in xrange(T):
        N, M = [int(x) for x in raw_input().split()]
        a = [int(x) for x in raw_input().split()]
        for i in xrange(N):
            M_mod = M % N
            M_div = M / N
            res = list(a)
            a_cache = {}  # intialize cache
            cpt = 1
            for j in xrange(N):
                ind = (j + i) % N
                if M_mod == 0:
                    cpt = 0
                else:
                    M_mod -= 1
                res[ind] = c_sum(a, ind, i, (i + N - 1) % N, N, M_div + cpt, a_cache)
            print ' '.join(map(str, res))
        if t < (T - 1): print ""


cal_sum()
