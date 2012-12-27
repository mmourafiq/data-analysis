import time


def check_nbr(nbr, nbrs, K):
    """
    checks if we could find a potential diff
    only compare nbr with the lowest nbr in the list
    """
    if nbr - nbrs[0] >= K:
        return True


def generate_indices(low_val, high_val):
    """
    given a list and a law value and high value, generate four indices that cut the interval by four    
    """
    step = int(round((high_val - low_val) / 4))
    return low_val, low_val + step, low_val + 2 * step, low_val + 3 * step, high_val


def dichotomie(nbr, nbrs, K, low_val, high_val, itr):
    """
    proceed by binary search, recursion shouldn't go beyond the limit itr
    for the sake of optimization, we will cut each intervall by 4 
    """
    itr += 1
    ind1, ind2, ind3, ind4, ind5 = generate_indices(low_val, high_val)
    if ind2 == 0 or ind1 >= ind2 or ind2 >= ind3 or ind3 >= ind4 or ind4 >= ind5 or itr == 100:  # can't be divided by 4, iterate
        for i in range(high_val, low_val - 1, -1):
            if nbr - nbrs[i] == K:
                return True
                break
        return False
    elif nbr - nbrs[ind4] == K:  # first quarter border
        return True
    elif nbr - nbrs[ind4] > K:  # first quarter
        return dichotomie(nbr, nbrs, K, ind4, ind5, itr)
    elif nbr - nbrs[ind3] == K:  # 2d quarter border
        return True
    elif nbr - nbrs[ind3] > K:  # 2d quarter
        return dichotomie(nbr, nbrs, K, ind3, ind4, itr)
    elif nbr - nbrs[ind2] == K:  # 3d quarter border
        return True
    elif nbr - nbrs[ind2] > K:  # 3d quarter
        return dichotomie(nbr, nbrs, K, ind2, ind3, itr)
    elif nbr - nbrs[ind1] == K:  # 4th quarter border
        return True
    elif nbr - nbrs[ind1] > K:  # 4th quarter
        return dichotomie(nbr, nbrs, K, ind1, ind1, itr)
    else:
        return False


def diffs():
    N, K = raw_input().split()
    N, K = int(N), int(K)
    nbrs = [int(n) for n in raw_input().split()]
    nbrs.sort()
    len_nbrs = len(nbrs)
    sum_diff = 0
    i = len_nbrs - 1
    while i > 0:
        itr = 0
        nbr = nbrs[i]
        if i / 10 > 10000:
            itr = 0
        elif i / 10 > 1000:
            itr = 1
        elif i / 10 > 100:
            itr = 2
        elif i / 10 > 10:
            itr = 3
        else:
            itr = 4
        if not check_nbr(nbr, nbrs, K):
            break
        if dichotomie(nbr, nbrs, K, 0, i - 1, itr=0):
            sum_diff += 1
        i -= 1
    return sum_diff


t = time.clock()
print diffs()
print time.clock() - t
