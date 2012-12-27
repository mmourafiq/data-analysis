# -*- coding: utf-8 -*-
"""
Created on Jan 01, 2013

@author: Mourad Mourafiq

About: This is an attempt to solve the Quora challenge Typehead.
"""

GO_ROOM = 0
NOGO_ROOM = 1
ENTRY_ROOM = 2
EXIT_ROOM = 3


class Room(object):
    """
    Room
    
    @type _x: int
    @param _x: x coordiante
      
    @type _y: int
    @param _y: y coordiante
    
    @type _type : int
    @param _type: the type of the node (0 1 2 3)
    
    
    @type _visited : boolean
    @param _visited: track if the room was visited
    
    @type _neighbours: list
    @param _neighbours: the neighbours rooms   
    """

    def __init__(self, type):
        self._type = type
        self._neighbours = []
        self._visited = False

    def add(self, neighbour):
        self._neighbours.append(neighbour)

    def init(self):
        self._neighbours = []

    def visit(self):
        self._visited = True

    def unvisit(self):
        self._visited = False

    def is_visited(self):
        return True if self._visited else False

    def is_exit(self):
        return True if self._type == EXIT_ROOM else False

    def is_entry(self):
        return True if self._type == ENTRY_ROOM else False

    def is_nogo(self):
        return True if self._type == NOGO_ROOM else False


class Cooling(object):
    """
    backtracking solution to datacenter cooling
    
    @type _rooms: dict
    @param _rooms: dictionary of the rooms of the datacenter
    
    
    @type _entry: tuple
    @param _entry: entry room coordiante
    
    @type _nbr_rooms: int
    @param _nbr_rooms: number of room in our datacenter
    
    @type _nbr_rooms_visited: int
    @param _nbr_rooms_visited: number of room visited so far
    
    @type _nbr_lines: int
    @param _nbr_lines: number of lines in our datacenter
    
    @type _nbr_columns: int
    @param _nbr_columns: number of columns in our datacenter
    
    @type _nbr_ways: int
    @param _nbr_ways: number of ways (result)  
    """

    def __init__(self, nbr_lines, nbr_columns):
        self._rooms = {}
        self._entry = (0, 0)
        self._nbr_rooms = nbr_lines * nbr_columns
        self._nbr_rooms_visited = 1
        self._nbr_lines = nbr_lines
        self._nbr_columns = nbr_columns
        self._nbr_ways = 0

    def add(self, type, line, column, look_for_entry=True):
        self._rooms[(line, column)] = Room(type)
        if look_for_entry:
            if self._rooms[(line, column)].is_entry():
                self._entry = (line, column)
                look_for_entry = False

    def _construct_neighbours(self, coord):
        l, c = coord
        room = self._rooms[(l, c)]
        room.init()
        if l > 0:
            if not (self._rooms[(l - 1, c)].is_nogo() or self._rooms[(l - 1, c)].is_visited()):
                room.add((l - 1, c))
        if l + 1 < self._nbr_lines:
            if not (self._rooms[(l + 1, c)].is_nogo() or self._rooms[(l + 1, c)].is_visited()):
                room.add((l + 1, c))
        if c > 0:
            if not (self._rooms[(l, c - 1)].is_nogo() or self._rooms[(l, c - 1)].is_visited()):
                room.add((l, c - 1))
        if c + 1 < self._nbr_columns:
            if not (self._rooms[(l, c + 1)].is_nogo() or self._rooms[(l, c + 1)].is_visited()):
                room.add((l, c + 1))

    def _visit(self, room):
        room.visit()
        self._nbr_rooms_visited += 1

    def _unvisit(self, room):
        room.unvisit()
        self._nbr_rooms_visited -= 1

    def find_way(self, current_room_coord=None):
        if current_room_coord is None:
            current_room_coord = self._entry
            self._visit(self._rooms[current_room_coord])
        # check if exist
        elif self._rooms[current_room_coord].is_exit():
            if self._nbr_rooms_visited == self._nbr_rooms:
                self._nbr_ways += 1
                return True
            else:
                return False
        # not exit yet, try this room's neighbours
        self._construct_neighbours(current_room_coord)
        current_room = self._rooms[current_room_coord]
        for neighbour in current_room._neighbours:
            self._visit(self._rooms[neighbour])
            self.find_way(neighbour)
            self._unvisit(self._rooms[neighbour])
            # at this point we couldn't find the exit
        return False


W, H = [int(x) for x in raw_input().split()]
cool = Cooling(H, W)
for l in xrange(H):
    rooms = [int(x) for x in raw_input().split()]
    for c in xrange(W):
        cool.add(rooms[c], l, c)
cool.find_way()
print cool._nbr_ways