# -------------------------------------------------------------------------------
# Name:        simple implementation if page rank
#
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------

from __future__ import division
from data_analysis import jaccard_sim
from numpy import *

# example of set of pages belonging to the same topic (the simple topic sensitive page rank version)
S = set(('2', '4'))
Es = matrix([[0], [1], [0], [1]])


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
    elements_length = len(matrix)
    eigenvectors = (1 / elements_length) * mat(ones((elements_length, 1)))
    if S and taxation:
        taxation_v = (1 - b) / len(S) * Es
    else:
        taxation_v = (1 - b) / elements_length * mat(ones((elements_length, 1))) if taxation else mat(
            ones((elements_length, 1))) * 0

    eigenvectors_p = mat(ones((elements_length, 1))) * 0
    itr = 0
    while (eigenvectors_p != eigenvectors).any() and itr < nbr_iterations:
        if (eigenvectors_p != (mat(ones((elements_length, 1))) * 0)).any(): eigenvectors = eigenvectors_p;
        eigenvectors_p = matrix_vector_multiplication(matrix, eigenvectors, elements_length, b, taxation_v)
        itr += 1
    if verbose: print eigenvectors
    return eigenvectors


def matrix_vector_multiplication(matrix, vector, length, b, taxation_v):
    """
        calculate the multiplication of matrix by vector
    """
    return b * matrix * vector + taxation_v


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

#exemple of sets of keywords, to be used for the advanced page rank
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
    elements_length = len(matrix)
    i = 0
    for s in S:
        Esp = [0] * elements_length
        #calculate the jaccard similarity for each page and set and
        for p in range(elements_length):
            Esp[p] = jaccard_sim(P[p], s)
        Esp = mat(Esp)
        print s
        print Esp
        #calculate the page rank for each topic
        page_rank(matrix, taxation=True, b=b, Es=Esp.getT(), S=S[i], nbr_iterations=10000000, verbose=True)
        i += 1


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

    sm = (pr - tr) / pr
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
    elements_length = len(L)
    L_t = L.getT()
    H = mat(ones((elements_length, 1)))
    H_s = 0 * H
    A = [0] * H
    T = [0] * H
    itr = 0
    while (H != H_s).any() and itr < nbr_iterations:
        if (H_s != 0 * mat(ones((elements_length, 1)))).any(): H = H_s;
        A = matrix_vector_multiplication(L_t, H, elements_length, 1, T)
        m = A.max()
        A = A / m
        H_s = matrix_vector_multiplication(L, A, elements_length, 1, T)
        m = H_s.max()
        H_s = H_s / m
        itr += 1
    A = matrix_vector_multiplication(L_t, H, elements_length, 1, T)
    m = A.max()
    A = A / m
    if verbose:
        print H
        print A


def test_construct():
    construct_web(4, 0.8, verbose=True)


def test_page_rank():
    m = matrix([[0, 0.5, 0, 0], [1 / 3, 0, 0, 0.5], [1 / 3, 0, 1, 0.5], [1 / 3, 0.5, 0, 0]])
    page_rank(m, taxation=True, b=0.85, verbose=True)
    page_rank(m, taxation=True, b=0.85, Es=Es, S=S, verbose=True)


def test_page_rank_advanced():
    m = matrix([[0, 0.5, 0, 0], [1 / 3, 0, 0, 0.5], [1 / 3, 0, 1, 0.5], [1 / 3, 0.5, 0, 0]])
    P = tuple((tuple(('1', '2', '3', '4')), tuple(('0', '6', '7', '8')), tuple(('2', '5', '9', '10')),
               tuple(('2', '5', '9', '10', '0'))))
    page_rank_advanced(m, b=0.85, P=P, S=Sk, nbr_iterations=100000, verbose=True)


def test_sapm_farm():
    spam_farm(Pa=10, Ps=30, Pn=500, b=0.85, verbose=True)


def test_spam_mass():
    m = matrix([[0, 0.5, 0, 0], [1 / 3, 0, 0, 0.5], [1 / 3, 0, 1, 0.5], [1 / 3, 0.5, 0, 0]])
    return spam_mass(m, taxation=True, b=0.8, Ts=Es, Tp=S, verbose=True)


if __name__ == '__main__':
    test_construct()
    test_page_rank()
    test_page_rank_advanced()
    test_sapm_farm()
    test_spam_mass()
    
