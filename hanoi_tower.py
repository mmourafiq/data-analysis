#-------------------------------------------------------------------------------
# Name:        cryptarithmetic
# 
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq 
#-------------------------------------------------------------------------------
#!/usr/bin/env python
RODS = 'ABCDEFGHIJKLM'
def hanoi_tower(nbr_disks=5, nbr_rods=6):
    """
    Resolves the hanoi tower problem for n rods and n disks.
    goal is to move all disks from the left rod to the right rod 
    """
    goal = ['']*nbr_rods
    start = ['']*nbr_rods
    start[0] = RODS[0:nbr_disks]
    goal[-1] = RODS[0:nbr_disks]
    goal = tuple(goal)
    explored = set() # set of explored paths
    paths = [[ start ]]
    while paths:
        to_explore = paths.pop(0)
        current_state = to_explore[-1]
        for (state, action) in next_state(current_state, nbr_disks).items():
            if state not in explored:
                explored.add(state)
                path2 = to_explore + [action, state]
                if goal == state:
                    return path2
                else:
                    paths.append(path2)
    return []
        
def next_state(state, nbr_disks):
    result = {}
    for i in range(nbr_disks+1):        
        if state[i] != '':
            i_disk = state[i][-1] 
            for j in range(nbr_disks+1):                
                j_disk = state[j][-1] if state[j] != '' else state[j]  
                if i != j and i_disk > j_disk:
                    c_state = list(state)
                    c_state[i] = state[i][:-1]
                    c_state[j] = state[j] + i_disk 
                    result[tuple(c_state)] = 'move %s => %s' % (i_disk, j+1)

    return result
    
print hanoi_tower()
