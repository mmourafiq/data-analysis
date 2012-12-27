def n_div_P(n, P):
    if n >= P:
        j = 0
        m = n % P
        q = n / P
        j = q * (P - m - 1)
        return j + ((m + 1) * n_div_P(q, P))
    else:
        return 0


def n_C_p():
    T = int(raw_input())
    result = []
    for i in range(T):
        n, P = raw_input().split()
        n, P = int(n), int(P)
        j = n_div_P(n, P)
        result.append(j)
    for i in range(T):
        print result[i]


n_C_p()
