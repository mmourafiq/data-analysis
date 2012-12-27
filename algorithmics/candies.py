import collections


def candies():
    N = int(raw_input())
    next = collections.defaultdict(int)
    to_update = collections.defaultdict(int)

    def update(prev, current):
        if current in to_update:
            for i in range(to_update[current], current):
                next[i] += 1
        else:
            next[prev] += 1
            if prev >= 1 and next[prev] == next[prev - 1] and f[prev] < f[prev - 1]:
                update(prev - 1, current)
            else:
                to_update[current] = prev

    f = []
    for i in range(N):
        current = int(raw_input())
        f.append(current)
        if i == 0:
            next[i] = 1
            continue
        prev = f[i - 1]
        if current <= prev:
            next[i] = 1
            if next[i - 1] == 1:
                if current < prev: update(i - 1, i)
                # else: next[i] += 1
        elif current > prev:
            next[i] = next[i - 1] + 1

    print sum(next.values())


candies()
