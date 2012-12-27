# circle sum
def cal_sum():
    T = int(raw_input())

    def c_sum(a, N, M):
        res = []
        for i in xrange(N):
            res.append(list(a))
        for i in xrange(M):
            for j in xrange(N):
                res[j][((i + j) % N)] += (res[j][((i + j - 1) % N)] + res[j][((i + j + 1) % N)])
                res[j][((i + j) % N)] %= 1000000007
        for i in xrange(N):
            print ' '.join(map(str, res[i]))

    for t in xrange(T):
        N, M = [int(x) for x in raw_input().split()]
        a = [int(x) for x in raw_input().split()]
        c_sum(a, N, M)
        if t < (T - 1): print ""


cal_sum()
