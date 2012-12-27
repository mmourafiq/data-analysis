# circle sum

import numpy as nm


def cal_sum():
    T = int(raw_input())

    def list_mat(n, m_div, m_mod):
        a_n = []
        if m_div > 0:
            for i in xrange(n):
                a_i = nm.eye(n, dtype=nm.int)
                i_l = (i - 1) % n
                i_r = (i + 1) % n
                a_i[i_r][i] = 1
                a_i[i_l][i] = 1
                a_n.append(a_i)
        else:
            for i in xrange(n):
                a_i = nm.eye(n, dtype=nm.int)
                for j in xrange(m_mod):
                    i_l = (i + j - 1) % n
                    i_r = (i + j + 1) % n
                    a_i[i_r][i] = 1
                    a_i[i_l][i] = 1
                a_n.append(a_i)
        return a_n

    def mat_mult(n, a, a_n, ind, m_div, m_mod):
        res = nm.mat(nm.eye(n), dtype=nm.int)
        if m_div > 0:
            for i in xrange(n):
                j = (i + ind) % n
                res *= nm.mat(a_n[j])
            res = res ** m_div
        for i in xrange(m_mod):
            j = (i + ind) % n
            res *= nm.mat(a_n[j])
        return a * res

    for t in xrange(T):
        N, M = [int(x) for x in raw_input().split()]
        a = [int(x) for x in raw_input().split()]
        M_mod = M % N
        M_div = M / N
        a_n = list_mat(N, M_div, M_mod)
        for i in xrange(N):
            res = nm.nditer(mat_mult(N, a, a_n, i, M_div, M_mod))
            print ' '.join(map(str, res))
        if t < (T - 1): print ""


cal_sum()
