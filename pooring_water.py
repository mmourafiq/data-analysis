#-------------------------------------------------------------------------------
# Name:        palindromes
# 
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq 
#-------------------------------------------------------------------------------
#!/usr/bin/env python
def pooring_prob(size_x, size_y, goal, start=(0, 0)):
    """
    Resolves the pooring problem for two glasses x & y.
    goal is the size we are looking for.
    size_x & size_y are respectively the size of the glass x, glass y respectively. 
    """
    if goal in start:
        return [start]
    explored = set()#set of visited states
    paths = [ [start] ]
    while paths:
        to_explore = paths.pop(0)
        (x, y) = to_explore[-1]
        for (state, action) in next_state(x, y, size_x, size_y).items():
            if state not in explored:
                explored.add(state)
                path2 = to_explore + [action, state]
                if goal in state:
                    return path2
                else:
                    paths.append(path2)
                    
    return []

def next_state(x, y, size_x, size_y):
    assert x <= size_x and y <= size_y
    return {
             (0, x + y) if x+y <= size_y else (x - (size_y - y), size_y) :  'x->y',
             (y + x, 0) if x+y <= size_x else (size_x, y - (size_x - x)) :  'y->x',
             (size_x, y) : 'fill x', (x, size_y) : 'fill y',
             (0, y) : 'empty x', (x, 0) : 'empty y',
             }
    
print pooring_prob(440, 900, 600)
