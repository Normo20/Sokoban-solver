# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:02:35 2020

@author: User
"""

import search 
import sokoban
import math
from search import astar_graph_search as astar_graph

wh = Warehouse()
wh.load_warehouse("./warehouses/warehouse_03.txt")
print(wh)
dst= (1, 1)

class FindPathProblem(search.Problem):
    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse




offset_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]
bad_cells = None





def heuristic(n):
        state = n.state
        # distance = sqrt(xdiff^2 + ydiff^2). Basic distance formula heuristic.
        return math.sqrt(((state[1] - dst[1]) ** 2)
                         + ((state[0] - dst[0]) ** 2))

dst = (dst[1], dst[0])  # Destination is given in (row,col), not (x,y)

    # Use an A* graph search on the FindPathProblem search
node = astar_graph(FindPathProblem(wh.worker, wh, dst),
                       heuristic)

    # If a node was found, this is a valid destination
a= node is not None

#--------------------------------------------------------------------------------------------------------------------------


