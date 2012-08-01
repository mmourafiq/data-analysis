#-------------------------------------------------------------------------------
# Name:        graph analysis
#
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq 
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from __future__ import division
import random
import heapq

def rand_weight_link(graph, node1, node2):
    """
    Create a link between node1 and node2
    """
    if node1 not in graph:
        graph[node1] = {}
    graph[node1][node2] = random.randint(1, 10)
    if node2 not in graph:
        graph[node2] = {}
    graph[node2][node1] = random.randint(1, 10)

def link(graph, node1, node2):
    """
    Create a link between node1 and node2
    """
    if node1 not in graph:
        graph[node1] = {}
    graph[node1][node2] = 1 
    if node2 not in graph:
        graph[node2] = {}
    graph[node2][node1] = 1

def add_node(graph_to, graph_from, node):
    if node not in graph_to:
        graph_to[node] = graph_from[node]
        for neighbor in graph_to[node].keys():
            graph_to = add_node(graph_to, graph_from, neighbor)
    return graph_to
        
        
def shortest_path(graph, node1, node2):
    """
    Finds the shortest path from node1 in node 2 in graph.
    """        
    if node1 == node2:
        return [node1]
    explored = []
    to_explore = [[node1]]
    while to_explore:
        path = to_explore.pop(0)
        s = path[-1]
        for successor in graph[s].keys():
            if successor not in explored:
                explored.append(successor)
                path2 = path + [successor]
                if node2 == successor:
                    return path2
                to_explore.append(path2)
    return []
            
def longest_path(graph, node=None):
    """
    Returns the longest path in the graph if node is None
    I f node is not None, then it returns the longest path from node
    """
    if node is not None:
        return max([shortest_path(graph, node, successor) for successor in graph.keys()], key=len)
    return max([shortest_path(graph, a, b) for a in graph.keys() for b in graph.keys()], key=len)

def centrality(graph, node):
    """
    Returns the centrality of node in graph
    """    
    return sum([len(shortest_path(graph, node, successor)) for successor in graph.keys()])/len(graph.keys())

def indep_graphs(graph): 
    """
    Returns the independent graphs in the current graph
    """
    graphs = []     
    def which_graph(node):
        for g in graphs:
            if node in g: return g 
        return {}
        
    for node in graph.keys():
        g = add_node(which_graph(node), graph, node)
        if g not in graphs: graphs.append(g)        
    return graphs

def graph_for_node(graph, node):
    """
    Returns the independent graph containing node
    """
    return  add_node({}, graph, node)    
        
def check_pairwise_connectivity(graph, node1, node2):
    """
    checks the connectivity between two nodes, 
    and returns True if connected, otherwise False    
    """
    return True if node2 in graph_for_node(graph, node1) else False
    
def clustering_coef(graph, node, verbose=False):
    """
    calculates the clustering coef for a particular node in the graph
     let Dn = node degree
         Vn = number of links between neighbors of the node
    """
    neighbors = graph[node].keys()
    Dn = len(neighbors)
    if Dn == 0 : return Dn;    
    Vn = 0
    for neighbor1 in neighbors:
        index1 = neighbors.index(neighbor1)
        for neighbor2 in neighbors:
            index2 = neighbors.index(neighbor2)
            if index1 < index2 and neighbor2 in graph[neighbor1]: Vn += 1
    coef = (2 * Vn) / (Dn * (Dn - 1))
    if verbose: print '%s\'s degree : %s, links between neighbors : %s. Culestering coef : %s' % (node, Dn, Vn, coef)    
    return coef 

def random_clustering_coef(graph, node, nbr_iterations=1000000):
    """
    calculates the estimate clustering coef for a particular node in the graph
    """
    vindex = {}
    d = 0
    for w in graph[node].keys():
        vindex[d] = w
        d += 1
    
    total = 0
    for i in range(1,nbr_iterations):
        if d > 1:
            pick = random.randint(0,d-1)
            v1 = vindex[pick]
            v2 = vindex[(pick+random.randint(1,d-1))%d]
            if v2 in graph[v1]: total += 1
        print i, (total+0.0)/i

def average_cluestering(graph, verbose=True):
    average = sum([clustering_coef(graph, node, verbose=verbose) for node in graph])/len(graph)
    if verbose: print average
    return average

def dijkstra(graph, node):
    """
    Simulate the dijkstra algorithm in a graph
    """
    distance_to = {}
    distance_to[node] = 0    
    distance_path = {}
    while (distance_to):
        #in case we have a disjoint graph
        op_node = min_distance(distance_to)
        distance_path[op_node] = distance_to[op_node]
        del distance_to[op_node]
        for x, x_len in graph[op_node].items():
            if x not in distance_path:
                if x not in distance_to:
                    distance_to[x] = distance_path[op_node] + x_len
                elif distance_to[x] > distance_path[op_node] + x_len:
                    distance_to[x] = distance_path[op_node] + x_len
    return distance_path

def min_distance(distances):
    """
    return the element with the min distance
    """
    min = (-1, -1)
    for node, node_len in distances.items():
        if min[1] > node_len or min[1] == -1:
            min = (node, node_len)
    return min[0]

def dijkstra_heap(graph, node):
    """
    Simulate the dijkstra algorithm in a graph
    """
    track_distance = {}
    track_distance[node] = 0
    distance_to = []    
    heapq.heappush(distance_to, (0,node))
    distance_path = {}
    while (distance_to):
        #in case we have a disjoint graph
        #op_node = min_distance(distance_to)
        #distance_path[op_node] = distance_to[op_node]
        #del distance_to[op_node]
        ind, op_node = heapq.heappop(distance_to)
        if op_node not in distance_path or ind < distance_path[op_node]:
            distance_path[op_node] = ind
        for x, x_len in graph[op_node].items():
            if x not in distance_path:
                if x not in track_distance:
                    track_distance[x] = distance_path[op_node] + x_len
                    heapq.heappush(distance_to, (track_distance[x], x))                                        
                elif track_distance[x] > distance_path[op_node] + x_len:
                    track_distance[x] = distance_path[op_node] + x_len
                    heapq.heappush(distance_to, (track_distance[x], x))  
    return distance_path

# heap functions 

def parent(i): return (i-1)/2
def left_child(i): return 2*i+1
def right_child(i): return 2*i+2
def is_leaf(heap_list,i): return (left_child(i) >= len(heap_list)) and (right_child(i) >= len(heap_list))
def has_one_child(heap_list,i): return (left_child(i) < len(heap_list)) and (right_child(i) >= len(heap_list))

# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children
def down_heapify(heap_list, i):
    # If i is a leaf, heap property holds
    if is_leaf(heap_list, i): 
        return
    # If i has one child...
    if has_one_child(heap_list, i):
        # check heap property
        if heap_list[i] > heap_list[left_child(i)]:
            # If it fails, swap, fixing i and its child (a leaf)
            (heap_list[i], heap_list[left_child(i)]) = (heap_list[left_child(i)], heap_list[i])
        return
    # If i has two children...
    # check heap property
    if min(heap_list[left_child(i)], heap_list[right_child(i)]) >= heap_list[i]: 
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if heap_list[left_child(i)] < heap_list[right_child(i)]:
        # Swap into left child
        (heap_list[i], heap_list[left_child(i)]) = (heap_list[left_child(i)], heap_list[i])
        down_heapify(heap_list, left_child(i))
        return
    else:
        (heap_list[i], heap_list[right_child(i)]) = (heap_list[right_child(i)], heap_list[i])
        down_heapify(heap_list, right_child(i))
        return


def build_heap(heap_list):
    for i in range(len(heap_list)-1, -1, -1):
        down_heapify(heap_list, i)
    return heap_list

def remove_min_heap(heap_list):
    heap_list[0] = heap_list.pop()
    down_heapify(heap_list, 0)
    return heap_list

def sort_heap(heap_list):
    sorted_heap = []    
    while len(heap_list) > 0:
        sorted_heap = heap_list.pop()
        remove_min_heap(heap_list)
    return sorted_heap


