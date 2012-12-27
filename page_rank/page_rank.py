# -------------------------------------------------------------------------------
# Name:        simple implementation if page rank
#
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from __future__ import division
import multiprocessing
import numpy
import random
from map_reduce import MapReduce
from jaccard_similarity import jaccard_sim

# example of set of pages belonging to the same topic (the simple topic sensitive page rank version)
S = set(('2', '4'))
Es = [0, 1, 0, 1]


def page_rank(matrix, taxation=False, b=1, Es=[], S=set(), nbr_iterations=10000000, verbose=False):
    """
        calculate the page rank for each element based on the matrix in input
        we should validate if the matrix is stochastic
        if not we use the taxation method to ovoid dead ends (introducing the random surfers)
            v' = Mv + (1-b)e/n
            v : eigenvector
            The term (1-b)e/n is a vector each of whose components has value (1-b)/n and
            represents the introduction, with probability 1 - b, of a new random surfer at
            a random page.
        The mathematical formulation for the iteration that yields topic-sensitive
        PageRank is similar to the equation we used for general PageRank. The only
        difference is how we add the new surfers. Suppose S is a set of integers consisting
        of the row/column numbers for the pages we have identified as belonging to a
        certain topic (called the teleport set). Let eS be a vector that has 1 in the
        components in S and 0 in other components. Then the topic-sensitive Page-
        Rank for S is the limit of the iteration
            v' = bMv + (1 - b)eS/|S|
        Here, as usual, M is the transition matrix of the Web, and |S| is the size of set
        S.
    """
    elements_length = len(matrix[0])
    eigenvectors = [1 / elements_length] * elements_length
    if Es and taxation:
        taxation_v = [((1 - b) / len(S) * e) for e in Es]
    else:
        taxation_v = [(1 - b) / elements_length] * elements_length if taxation else [0] * elements_length

    eigenvectors_p = [0] * elements_length
    itr = 0
    # initializing map reduce
    mapper = MapReduce(page_rank_calculation, page_rank_vector)
    while eigenvectors_p != eigenvectors and itr < nbr_iterations:
        if eigenvectors_p != [0] * elements_length: eigenvectors = list(eigenvectors_p);
        for k, v in mapper([(i, eigenvectors, matrix, taxation_v, b) for i in range(elements_length)]):
            eigenvectors_p[k] = v
        itr += 1
    if verbose: print eigenvectors
    return eigenvectors


def page_rank_vector(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    key, occurances = item
    return (key, sum(occurances))


def page_rank_calculation(itemi):
    """Read a file and return a sequence of (word, occurances) values.
    """
    item, eigenvectors, matrix, taxation_v, b = itemi
    elements_length = len(matrix)
    # print multiprocessing.current_process().name, 'calculating', item
    output = []
    vector_p = 0
    for j in range(elements_length):
        vector_p += eigenvectors[j] * matrix[item][j] * b
    vector_p += taxation_v[item]
    output.append((item, vector_p))
    return output


def matrix_vector_multiplication(matrix, vector, length, b, taxation_v):
    """
        calculate the multiplication of matrix by vector
    """
    vector_p = [0] * length
    for i in range(length):
        for j in range(length):
            vector_p[i] += vector[j] * matrix[i][j] * b
        vector_p[i] += taxation_v[i]
    return vector_p


def construct_web(n, b, nbr_iterations=100000, verbose=False):
    """
    Web consists of a clique (set of nodes with all possible arcs from one to another)
    of n nodes and a single additional node that is the successor of each of the n nodes
    in the clique. Determine the PageRank of each page, as a function of n
    and ?.
    """
    all_nodes = 1 / (n + 1)
    all_nodes_p = 0
    last_node = 1 / (n + 1)
    last_node_p = 0
    itr = 0
    while (all_nodes != all_nodes_p or last_node != last_node_p) and itr < nbr_iterations:
        if all_nodes_p != 0: all_nodes = all_nodes_p;
        if last_node_p != 0: last_node = last_node_p;
        all_nodes_p = b * all_nodes * ((n - 1) / n) + (1 - b) / (1 + n)
        last_node_p = b * last_node + (1 - b) / (1 + n)
        itr += 1
    if verbose:
        print all_nodes
        print last_node
    return all_nodes


# exemple of sets of keywords, to be used for the advanced page rank
Sk = tuple((tuple(('0', '6', '7')), tuple(('1', '3', '4', '8')), tuple(('2', '5', '9', '10'))))


def page_rank_advanced(matrix, b=1, P=set(), S=set(), nbr_iterations=100000, verbose=False):
    """
        calculation of the topic sensitive page rank.
        S is the set of sets of topics
        P is set of topic keywords for each page
        the algorithm we shall implement is the following:

                => calculate the jackard similarity for P and Si
                => classify the page for a topic
                =>construct Es, such that is the set of corresponding teleport surfurs for each set of topics
    """
    elements_length = len(matrix[0])
    topics_length = len(S)
    Es = []
    #calculate the jaccard similarity for each page and set and
    for s in S:
        Esp = [0] * elements_length
        for p in range(elements_length):
            Esp[p] = jaccard_sim(P[p], s)
        Es.append(Esp)
        print s
        print Esp
    #calculate the page rank for each topic
    for i in range(topics_length):
        page_rank(matrix, taxation=True, b=b, Es=Es[i], S=S[i], nbr_iterations=10000000, verbose=True)


def spam_farm(Pa, Ps, Pn, b, verbose=False):
    """
        The spam farm consists of the spammer?s own pages "target page", organized in a special
        way, and some links from the accessible pages to the
        spammer?s pages. Without some links from the outside, the spam farm would
        be useless, since it would not even be crawled by a typical search engine.
        Concerning the accessible pages, it might seem surprising that one can affect
        a page without owning it. However, today there are many sites, such as
        blogs or newspapers that invite others to post their comments on the site. In
        order to get as much PageRank flowing to his own pages from outside, the
        spammer posts many comments.
        In the spam farm, there is one page, the target page, at which the spammer
        attempts to place as much PageRank as possible. There are a large number
        Ps of supporting pages, that accumulate the portion of the PageRank that is
        distributed equally to all pages
        Pa : is the amount of accessible pages
        Ps : the amount of supporting pages
        Pn : the amount of total pages in the web
            => we are looking for PR_t : wich is the page rank for the target page
        -the page rank of each supporting page is :
            b*PR_t + (1-b)/Pn
        Since the page rank of the target page comes from 3 sources:
            1. Pa from outside accessible pages
            2. b times the page rank of the supporting pages:
                    b*((b*PR_t)/Ps + (1-b)/Pn)
            3. (1-b)/Pn, the share of the fraction (1-b) of the page rank that belongs  to PR_t.
                is negligible and will be dropped to simplify the calculus

            => from (1) & (2) :
                PR_t = Pa + (b*Ps)*((b * PR_t)/Ps + (1-b)/Pn) + (1-b)/Pn
                PR_t = Pa/(1-b**2) + (b/(1+b))*(Ps/Pn)) + 1/(Pn*(1+b))
                PR_t = Pa/x + y*(Ps/Pn) + 1/(Pn*(1+b))
            where x = 1/(1- b**2) & y = b/(1+b)
    """
    x = 1 / (1 - b ** 2)
    x *= 100
    y = b / (1 + b)
    y *= 100
    PR_t = Pa / x + y * (Ps / Pn) + 1 / (Pn * (1 + b))
    if verbose:
        print 'Amplification of the external page rank contribution by %4.2f' % x
        print 'amount of PageRank that is %4.2f of the fraction Ps/n in the spam farm.' % y
        print 'page rank of target page %4.2f' % PR_t
    return PR_t


def trust_rank(matrix, b=0.8, Ts=[], Tp=set(), nbr_iterations=10000000, verbose=False):
    """
        TrustRank based on some teleport set of trustworthy pages.
        Computed the same way as a topic sensitive page rank. The only difference is that the
        teleport surfers are considered trustworthy pages
        Tp : trusted pages.
        Ts : trustworthy vector
    """
    return page_rank(matrix=matrix, taxation=True, b=b, Es=Ts, S=Tp, nbr_iterations=nbr_iterations, verbose=verbose)


def spam_mass(matrix, taxation=False, b=1, Es=[], S=set(), Ts=[], Tp=set(), nbr_iterations=10000000, verbose=False):
    """
        calculate the spam mass of a pages : (Pr - Tr) / Pr
    """
    pr = page_rank(matrix=matrix, taxation=True, b=b, Es=Es, S=S, nbr_iterations=nbr_iterations, verbose=verbose)
    tr = trust_rank(matrix=matrix, b=b, Ts=Ts, Tp=Tp, nbr_iterations=nbr_iterations, verbose=verbose)
    elements_length = len(matrix[0])
    sm = [0] * elements_length
    for i in range(elements_length):
        sm[i] = (pr[i] - tr[i]) / pr[i]
    if verbose: print sm;
    return sm


def hits(L, lam, mu, nbr_iterations=100000000, verbose=True):
    """
        Hiperlink induced topic search
        Computation of hubbiness and authority
        Authority : page's quality that tells you best about a topic
        Hubbiness : page's quality that tells you best about other pages and how to find them
        Authority of a page is the sum of predecessors's hubbiness
        Hubiness of a page is the sum of predecessors's authority
        L[i][j] = 1 if page_i link to page_j otherwise 0
    """
    elements_length = len(L[0])
    L_t = transpose(L, elements_length)
    H = [1] * elements_length
    H_s = [0] * elements_length
    A = [0] * elements_length
    T = [0] * elements_length
    itr = 0
    while H != H_s and itr < nbr_iterations:
        if H_s != [0] * elements_length: H = H_s;
        A = matrix_vector_multiplication(L_t, H, elements_length, 1, T)
        m = max(A)
        for i in range(elements_length):
            A[i] /= m
        H_s = matrix_vector_multiplication(L, A, elements_length, 1, T)
        m = max(H_s)
        for i in range(elements_length):
            H_s[i] /= m
        itr += 1
    A = matrix_vector_multiplication(L_t, H, elements_length, 1, T)
    m = max(A)
    for i in range(elements_length):
        A[i] /= m
    if verbose:
        print H
        print A


def transpose(matrix, elements_length, verbose=False):
    matrix_t = []
    for i in range(elements_length):
        t = [0] * elements_length
        for j in range(elements_length):
            t[j] = matrix[j][i]
        matrix_t.append(t)
    if verbose:
        print matrix
        print matrix_t
    return matrix_t


def test_construct():
    matrix = []
    matrix.append([0, 1 / 4, 1 / 4, 1 / 4, 0])
    matrix.append([1 / 4, 0, 1 / 4, 1 / 4, 0])
    matrix.append([1 / 4, 1 / 4, 0, 1 / 4, 0])
    matrix.append([1 / 4, 1 / 4, 1 / 4, 0, 0])
    matrix.append([1 / 4, 1 / 4, 1 / 4, 1 / 4, 0])
    page_rank(matrix, taxation=True, b=0.8, verbose=True)
    construct_web(4, 0.8, verbose=True)


def test_page_rank():
    matrix = []
    matrix.append([0, 1 / 2, 0, 0])
    matrix.append([1 / 3, 0, 0, 1 / 2])
    matrix.append([1 / 3, 0, 1, 1 / 2])
    matrix.append([1 / 3, 1 / 2, 0, 0])
    page_rank(matrix, taxation=True, b=0.85, verbose=True)
    page_rank(matrix, taxation=True, b=0.85, Es=Es, S=S, verbose=True)


def test_page_rank_advanced():
    matrix = []
    matrix.append([0, 1 / 2, 0, 0])
    matrix.append([1 / 3, 0, 0, 1 / 2])
    matrix.append([1 / 3, 0, 1, 1 / 2])
    matrix.append([1 / 3, 1 / 2, 0, 0])
    P = tuple((tuple(('1', '2', '3', '4')), tuple(('0', '6', '7', '8')), tuple(('2', '5', '9', '10')),
               tuple(('2', '5', '9', '10', '0'))))
    page_rank_advanced(matrix, b=0.85, P=P, S=Sk, nbr_iterations=100000, verbose=False)


def test_sapm_farm():
    spam_farm(Pa=10, Ps=30, Pn=500, b=0.855, verbose=True)


def test_spam_mass():
    matrix = []
    matrix.append([0, 1 / 2, 0, 0])
    matrix.append([1 / 3, 0, 0, 1 / 2])
    matrix.append([1 / 3, 0, 1, 1 / 2])
    matrix.append([1 / 3, 1 / 2, 0, 0])
    spam_mass(matrix, taxation=True, b=0.85, Ts=Es, Tp=S, verbose=True)


def test_hits():
    matrix = []
    matrix.append([0, 1, 1, 1, 0])
    matrix.append([1, 0, 0, 1, 0])
    matrix.append([0, 0, 0, 0, 1])
    matrix.append([0, 1, 1, 0, 0])
    matrix.append([0, 0, 0, 0, 0])
    hits(matrix, 0, 0)


if __name__ == '__main__':
    test_construct()
    test_page_rank()
    test_page_rank_advanced()
    test_sapm_farm()
    test_spam_mass()
    
