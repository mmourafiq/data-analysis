import collections

sample_input = """
20 19
2 1
3 1
4 3
5 2
6 5
7 1
8 1
9 2
10 7
11 10
12 3
13 7
14 8
15 12
16 6
17 6
18 10
19 1
20 8
"""
# expected return 4
N, M = raw_input().split()
summy = 0
forest = collections.defaultdict(list)
depth = collections.defaultdict(int)


def forest_construction():
    """
    construct the graph from std input
    """
    global head
    for i in range(int(M)):
        node2, node1 = raw_input().split()
        forest[node1].append(node2)


def nbr_nodes(node):
    """
    returns the number of nodes in the current sub-graph
    """
    nbr = 1
    for n in forest[node]:
        nbr += nbr_nodes(n)
    return nbr


def nodes_depth():
    """
    construct depth for each node
    """
    for node in forest.keys():
        depth[node] = nbr_nodes(node)


def get_head():
    """
    returns the head of the graph
    """
    head = ''
    max_v = 0
    for k, v in depth.items():
        if v > max_v:
            head = k
            max_v = v
    return head


def forest_slicing(node):
    """
    calculate the number of removed edges in such a forest.
    """
    summy = 0
    for n in forest[node]:  # direct successors
        if not n in depth:
            depth[n] = 1
        elif depth[n] % 2 == 0:
            summy += 1
            summy += forest_slicing(n)
        else:
            summy += forest_slicing(n)
    return summy


forest_construction()
nodes_depth()
print forest_slicing(get_head())
