from math import sqrt
from fractions import gcd


def get_factors(x):
    factors = set([x])

    sqrtX = int(sqrt(x))

    for i in range(1, sqrtX + 1):

        if x % i == 0:
            factors.add(i)
            factors.add(x / i)

    return factors


def friendly():
    _, friendly = [int(i) for i in raw_input().split()]
    unfriendlies = [int(i) for i in raw_input().split()]

    friendly_factors = get_factors(friendly)

    unfriendly_factors = set()

    for unfriendly in unfriendlies:
        g = gcd(friendly, unfriendly)

        unfriendly_factors.add(g)
        unfriendly_factors.update(get_factors(g))
    print len(friendly_factors - unfriendly_factors)


friendly()
