
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script.
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the
interface and results in a fail for the test of your code.
This is not negotiable!


'''

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files

import search

import sokoban

import copy

global actionD
actionDict = {'Up': (0, -1),
              'Down': (0, 1),
              'Left': (-1, 0),
              'Right': (1, 0)}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [('n10256989', 'James', 'Norman')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -




def taboo_cells(warehouse):
    '''
       Identify the taboo cells of a warehouse. A cell inside a warehouse is
       called 'taboo'  if whenever a box get pushed on such a cell then the puzzle
       becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
       When determining the taboo cells, you must ignore all the existing boxes,
       only consider the walls and the target  cells.
       Use only the following two rules to determine the taboo cells;
        Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
        Rule 2: all the cells between two corners along a wall are taboo if none of
                these cells is a target.

       @param warehouse:
           a Warehouse object with a worker inside the warehouse

       @return
          A string representing the puzzle with only the wall cells marked with
          a '#' and the taboo cells marked with a 'X'.
          The returned string should NOT have marks for the worker, the targets,
          and the boxes.
       '''

    # Fixed signs that are used for clarity


    targets = ['!', '.', '*']

    wall = '#'

    taboo_cell = 'X'


   #checks if cell is in corner
    def check_corner(warehouse, x_coord, y_coord, onWall=False):

        walls_left_or_right = 0

        walls_above_or_below = 0

        # check for walls on either side
        for (dx, dy) in [actionDict['Left'], actionDict['Right']]:
            if warehouse[y_coord + dy][x_coord + dx] == wall:
                walls_left_or_right += 1

        # checks for walls above and below
        for (dx, dy) in [actionDict['Up'], actionDict['Down']]:
            if warehouse[y_coord + dy][x_coord + dx] == wall:
                walls_above_or_below += 1


        if onWall:
            return (walls_above_or_below >= 1) or (walls_left_or_right >= 1)
        else:
            return (walls_above_or_below >= 1) and (walls_left_or_right >= 1)

    # Turn warehouse into an array

    warehouseStr = str(warehouse)

    # Remove boxes and player from warehouse and replaces it with blank space

    useless_signs = ["@", "$"]

    for char in useless_signs:
        warehouseStr = warehouseStr.replace(char, ' ')

    warehouse_2d = [list(row) for row in warehouseStr.split('\n')]


    def rule1(warehouse_2d):
        for y in range(len(warehouse_2d) - 1):
            inside = False
            for x in range(len(warehouse_2d[0]) - 1):

                if not inside:
                    if warehouse_2d[y][x] == wall:
                        inside = True
                else:
                    if all([cell == ' ' for cell in warehouse_2d[y][x:]]):
                        break
                    # changes cell is an empty square, then checks for corner
                    if warehouse_2d[y][x] not in targets:
                        if warehouse_2d[y][x] != wall:
                            if check_corner(warehouse_2d, x, y):
                                warehouse_2d[y][x] = taboo_cell
        return warehouse_2d


    def rule2(warehouse_2d):
        for y in range(1, len(warehouse_2d) - 1):
            for x in range(1, len(warehouse_2d[0]) - 1):
                if warehouse_2d[y][x] == taboo_cell and check_corner(warehouse_2d, x, y):
                    Column = [eachRow[x] for eachRow in warehouse_2d[y + 1:]]
                    Row = warehouse_2d[y][x + 1:]

                    # to check cells up and down
                    for next_square_y in range(len(Column)):
                        if Column[next_square_y] in targets or Column[next_square_y] == wall:
                            break

                        if Column[next_square_y] == taboo_cell and check_corner(warehouse_2d, x,
                                                                                       next_square_y + y + 1):
                            if all([check_corner(warehouse_2d, x, nextNextSquareY, True)
                                    for nextNextSquareY in range(y + 1, next_square_y + y + 1)]):
                                for edgeSquaresY in range(y + 1, next_square_y + y + 1):
                                    warehouse_2d[edgeSquaresY][x] = taboo_cell



                    # checks cells across from left to right
                    for nextSquare_x in range(len(Row)):

                        if Row[nextSquare_x] in targets or Row[nextSquare_x] == wall:
                            break

                        if Row[nextSquare_x] == taboo_cell and check_corner(warehouse_2d, x + nextSquare_x + 1, y):
                            if all([check_corner(warehouse_2d, nextNextSquare, y, True)
                                    for nextNextSquare in range(x + 1, nextSquare_x + x + 1)]):
                                for edgeSquares in range(x + 1, nextSquare_x + x + 1):
                                    warehouse_2d[y][edgeSquares] = taboo_cell


        return warehouse_2d

    warehouse_2d = rule2(rule1(warehouse_2d))

    # Converts back from 2d array to string for sanity_check

    taboo_wh = '\n'.join([''.join(line) for line in warehouse_2d])
    # Remove target squares
    for char in targets:
        taboo_wh = taboo_wh.replace(char, ' ')

    return taboo_wh







# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
       An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
       An instance contains information about the walls, the targets, the boxes
       and the worker.

       Your implementation should be fully compatible with the search functions of
       the provided module 'search.py'.

       Each SokobanPuzzle instance should have at least the following attributes
       - self.allow_taboo_push
       - self.macro

       When self.allow_taboo_push is set to True, the 'actions' function should
       return all possible legal moves including those that move a box on a taboo
       cell. If self.allow_taboo_push is set to False, those moves should not be
       included in the returned list of actions.

       If self.macro is set True, the 'actions' function should return
       macro actions. If self.macro is set False, the 'actions' function should
       return elementary actions.
       '''

    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.


    #initializing the warehouse and its variables
    def __init__(self, warehouse, targetPos=None, elem=True, ignore_taboo=False,push_costs = None):
        self.warehouse = warehouse
        self.tabooCells = taboo_cells(warehouse)
        self.initial = warehouse
        self.targetPos = targetPos
        self.elem = elem
        self.ignore_taboo = ignore_taboo
        self.push_cost = push_costs

    def actions(self, state):
        """
                Return the list of actions that can be executed in the given state.

                As specified in the header comment of this class, the attributes
                'self.allow_taboo_push' and 'self.macro' should be tested to determine
                what type of list of actions is to be returned.
                """
        actions = []
             #checks that worker isn't in a wall upon move
        if (tuple((state.worker[0], state.worker[1] - 1)) not in state.walls):
            #checks that worker isn't in a box upon move
            if (not self.targetPos and tuple((state.worker[0], state.worker[1] - 1)) in state.boxes):
                #does check not ignoring taboo
                if (not self.ignore_taboo and tuple(
                        (state.worker[0], state.worker[1] - 2)) not in state.boxes + state.walls):
                    actions.append('Up')
                    #does check ignoring taboo
                if (self.ignore_taboo and tuple(
                        (state.worker[0], state.worker[1] - 2)) not in state.boxes + state.walls):
                    actions.append('Up')
            elif (self.targetPos and tuple((state.worker[0], state.worker[1] - 1)) not in state.boxes):
                actions.append('Up')
                #checks not in the target position
            elif (not self.targetPos):
                actions.append('Up')

                   #does the same as above but for the down action
        if (tuple((state.worker[0], state.worker[1] + 1)) not in state.walls):
            if (not self.targetPos and tuple((state.worker[0], state.worker[1] + 1)) in state.boxes):
                if (not self.ignore_taboo and tuple(
                        (state.worker[0], state.worker[1] + 2)) not in state.boxes + state.walls):
                    actions.append('Down')
                if (self.ignore_taboo and tuple(
                        (state.worker[0], state.worker[1] + 2)) not in state.boxes + state.walls):
                    actions.append('Down')
            elif (self.targetPos and tuple((state.worker[0], state.worker[1] + 1)) not in state.boxes):
                actions.append('Down')
            elif (not self.targetPos):
                actions.append('Down')
        # does the same as above but for the left action
        if self.elem:
            if (tuple((state.worker[0] - 1, state.worker[1])) not in state.walls):
                if (not self.targetPos and tuple((state.worker[0] - 1, state.worker[1])) in state.boxes):
                    if (not self.ignore_taboo and tuple(
                            (state.worker[0] - 2, state.worker[1])) not in state.boxes + state.walls):
                        actions.append('Left')
                    if (self.ignore_taboo and tuple(
                            (state.worker[0] - 2, state.worker[1])) not in state.boxes + state.walls):
                        actions.append('Left')
                elif (self.targetPos and tuple((state.worker[0] - 1, state.worker[1])) not in state.boxes):
                    actions.append('Left')
                elif (not self.targetPos):
                    actions.append('Left')

            # does the same as above but for the right action
            if (tuple((state.worker[0] + 1, state.worker[1])) not in state.walls):
                if (not self.targetPos and tuple((state.worker[0] + 1, state.worker[1])) in state.boxes):
                    if (not self.ignore_taboo and tuple(
                            (state.worker[0] + 2, state.worker[1])) not in state.boxes + state.walls):
                        actions.append('Right')
                    if (self.ignore_taboo and tuple(
                            (state.worker[0] + 2, state.worker[1])) not in state.boxes + state.walls):
                        actions.append('Right')
                elif (self.targetPos and tuple((state.worker[0] + 1, state.worker[1])) not in state.boxes):
                    actions.append('Right')
                elif (not self.targetPos):
                    actions.append('Right')



        else:
            for box in state.boxes:
                left = (box[0] - 1, box[1])
                right = (box[0] + 1, box[1])
                up = (box[0], box[1] - 1)
                down = (box[0], box[1] + 1)



                if (left not in state.boxes and left not in state.walls):
                    if (right not in state.boxes and right not in state.walls):
                        if (("left" not in self.tabooCells or self.ignore_taboo) and can_go_there_col_row(state, right)):
                            actions.append((box, "Left"))
                        if (("right" not in self.tabooCells or self.ignore_taboo) and can_go_there_col_row(state, left)):
                            actions.append((box, "Right"))
                if (up not in state.boxes and up not in state.walls):
                    if ("down" not in state.boxes and down not in state.walls):
                        if (("up" not in self.tabooCells or self.ignore_taboo) and can_go_there_col_row(state, down)):
                            actions.append((box, "Up"))
                        if (("down" not in self.tabooCells or self.ignore_taboo) and can_go_there_col_row(state, up)):
                            actions.append((box, "Down"))

        return actions

    def result(self, state, action):


        next_state = state.copy()
        next_state.boxes = copy.copy(state.boxes)

        if (action in self.actions(next_state)):
            if (self.elem):
                worker = list(next_state.worker)

                if (action == "Up"):
                    worker[1] -= 1
                    if (tuple(worker) in next_state.boxes):
                        i = next_state.boxes.index(tuple(worker))
                        box = list(next_state.boxes[i])
                        box[1] -= 1
                        next_state.boxes[i] = tuple(box)
                if (action == "Down"):
                    worker[1] += 1
                    if (tuple(worker) in next_state.boxes):
                        i = next_state.boxes.index(tuple(worker))
                        box = list(next_state.boxes[i])
                        box[1] += 1
                        next_state.boxes[i] = tuple(box)


                if (action == "Left"):
                    worker[0] -= 1
                    if (tuple(worker) in next_state.boxes):
                        i = next_state.boxes.index(tuple(worker))
                        box = list(next_state.boxes[i])
                        box[0] -= 1
                        next_state.boxes[i] = tuple(box)
                if (action == "Right"):
                    worker[0] += 1
                    if (tuple(worker) in next_state.boxes):
                        i = next_state.boxes.index(tuple(worker))
                        box = list(next_state.boxes[i])
                        box[0] += 1
                        next_state.boxes[i] = tuple(box)


                next_state.worker = tuple(worker)

            else:
                i = next_state.boxes.index(action[0])
                box = list(next_state.boxes[i])

                if (action[1] == "Up"):
                    box[1] -= 1
                if (action[1] == "Down"):
                    box[1] += 1
                if (action[1] == "Left"):
                    box[0] -= 1
                if (action[1] == "Right"):
                    box[0] += 1


                next_state.boxes[i] = tuple(box)
                next_state.worker = action[0]

        return next_state

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        for box in state.boxes:
            if box in state.targets:
                continue
            else:
                return False
        return True




#heuristic function manhattan (check get_distance and manhattan for helpers)
    def h(self, node):

        warehouse = node.state
        worker = warehouse.worker
        boxes = warehouse.boxes
        targets = warehouse.targets

        heuristic = 0

        for box in boxes:
            boxMin = get_Distance(box, targets)
            heuristic += boxMin

        min = get_Distance(worker, boxes)
        heuristic += min



        return heuristic








# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''

        Determine if the sequence of actions listed in 'action_seq' is legal or not.

        Important notes:
          - a legal sequence of actions does not necessarily solve the puzzle.
          - an action is legal even if it pushes a box onto a taboo cell.

        @param warehouse: a valid Warehouse object

        @param action_seq: a sequence of legal actions.
               For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

        @return
            The string 'Impossible', if one of the action was not successul.
               For example, if the agent tries to push two boxes at the same time,
                            or push one box into a wall.
            Otherwise, if all actions were successful, return
                   A string representing the state of the puzzle after applying
                   the sequence of actions.  This must be the same string as the
                   string returned by the method  Warehouse.__str__()
        '''

    ##         "INSERT YOUR CODE HERE"

    boxes = list(warehouse.boxes)
    worker = list(warehouse.worker)
    warehouse = warehouse.copy(worker, boxes)

    for action in action_seq:
        # Checks that the move is possible
        # If it is not possible, return impossible
        if is_move_possible(warehouse, action):
            x, y = find_move(action)
            worker[0] += x
            worker[1] += y

            # Checks to see if boxes were pushed and if so pushes them
            for idx, box in enumerate(boxes):
                if box == (worker[0], worker[1]):
                    box_x = box[0] + x
                    box_y = box[1] + y
                    boxes[idx] = (box_x, box_y)

            warehouse = warehouse.copy(worker, boxes)
        else:
            return "Impossible"

    warehouse = warehouse.copy(worker, boxes)
    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''
        This function should solve using A* algorithm and elementary actions
        the puzzle defined in the parameter 'warehouse'.

        In this scenario, the cost of all (elementary) actions is one unit.

        @param warehouse: a valid Warehouse object

        @return
            If puzzle cannot be solved return the string 'Impossible'
            If a solution was found, return a list of elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        '''

    ##         "INSERT YOUR CODE HERE"

#uses astar search to find a solution to the puzzle
    sp = SokobanPuzzle(warehouse)
    sol = search.astar_graph_search(sp)
#if no solution is found returns impossible
    if sol is None:
        return 'Impossible'
    else:
        #returns solution if found
        return sol.solution()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def can_go_there_col_row(warehouse, dst):
    '''
    changes dst to column,row to match the rest of the code
    '''
    return can_go_there(warehouse, (dst[1], dst[0]))


def can_go_there(warehouse, dst):
    '''
        Determine whether the worker can walk to the cell dst=(row,column)
        without pushing any box.

        @param warehouse: a valid Warehouse object

        @return
          True if the worker can walk to cell dst=(row,column) without pushing any box
          False otherwise
        '''

    ##         "INSERT YOUR CODE HERE"

    def heuristic(node):
        # Using Manhattan Distance for heuristics
        nodeState = node.state
         #maths stuff
        a2 = (nodeState[0] - dst[0]) ** 2
        b2 = (nodeState[1] - dst[1]) ** 2
        manhattanDistance = (a2 + b2) ** 0.5

        return manhattanDistance

    worker = warehouse.worker
    node = search.astar_graph_search(Pathing(worker, warehouse, dst), heuristic)

    return node is not None




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''
      Solve using using A* algorithm and macro actions the puzzle defined in
      the parameter 'warehouse'.

      A sequence of macro actions should be
      represented by a list M of the form
              [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
      For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ]
      means that the worker first goes the box at row 3 and column 4 and pushes it left,
      then goes to the box at row 5 and column 2 and pushes it up, and finally
      goes the box at row 12 and column 4 and pushes it down.

      In this scenario, the cost of all (macro) actions is one unit.

      @param warehouse: a valid Warehouse object

      @return
          If the puzzle cannot be solved return the string 'Impossible'
          Otherwise return M a sequence of macro actions that solves the puzzle.
          If the puzzle is already in a goal state, simply return []
      '''

    ##         "INSERT YOUR CODE HERE"

    wh = warehouse
    sp = SokobanPuzzle(wh, elem=False)
     #searches for macro solution
    sol = search.astar_graph_search(sp)
#returns impossible if solution not found
    if sol is None:
        return 'Impossible'
    else:
        #returns the macro actions if it is possible
        M = []
        for action in sol.solution():
            M.append(((action[0][1], action[0][0]), action[1]))
        return M

 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def solve_weighted_sokoban_elem(warehouse, push_costs):

        '''
        In this scenario, we assign a pushing cost to each box, whereas for the
        functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were
        simply counting the number of actions (either elementary or macro) executed.

        When the worker is moving without pushing a box, we incur a
        cost of one unit per step. Pushing the ith box to an adjacent cell
        now costs 'push_costs[i]'.

        The ith box is initially at position 'warehouse.boxes[i]'.

        This function should solve using A* algorithm and elementary actions
        the puzzle 'warehouse' while minimizing the total cost described above.

        @param
         warehouse: a valid Warehouse object
         push_costs: list of the weights of the boxes (pushing cost)

        @return
            If puzzle cannot be solved return 'Impossible'
            If a solution exists, return a list of elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        '''

        ########################
        #This code doesn't work
        #:(
        #:(
        ########################

        #wh = warehouse.copy()
        #loads puzzle with push costs and taboo cells on
        #sp = SokobanPuzzle(wh, push_costs,elem=False, ignore_taboo=False)
        #searches for a solution
        #sol = search.astar_graph_search(sp)
        #steps = []
        # returns impossible if solution not found
        #if sol is None:
         #   return 'Impossible'
        #checks action seq
        #else:
         #   action_seq = steps[1:]
          #  if check_elem_action_seq(warehouse, action_seq) == 'Impossible':
           #     return 'Impossible'
            #else:
               #returns the shortest cost route and returns it
             #   for action in sol.solution():
              #      steps.append(((action[0][1], action[0][0]), action[1]))
               # return steps








# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#some random helper functions (all labeled for where they're used)

#heuristic helper
def manhattan(xcoord, ycoord):

    #This helper function calculates the returned distances

    #returns the distance between player and boxes or player and targets

    return abs(xcoord[0] - ycoord[0]) + abs(xcoord[1] - ycoord[1])

#heuristic helper
def get_Distance(start, locations):

    #The helper function finds the shortest distance between player
    #and boxes or player and targets

    #returns the shortest distance

    min_dist = 0

    for coor in locations:
        dist = manhattan(start, coor)
        if (dist < min_dist):
            min_dist = dist

    return min_dist

# check_elem_action helper
def find_move(action):

    #Helper function finds the position of x and y from action



    #returns x and y value after action

    x = 0
    y = 0
    if (action == "Up"):
        y -= 1
    elif (action == "Down"):
        y += 1
    elif (action == "Left"):
        x -= 1
    elif (action == "Right"):
        x += 1

    return x, y
# Check_elem_action helper

def is_move_possible(warehouse, action):

    #Helper function to see if the next move is possible with particular action
    #returns true if move is possible and false if not

    worker_x = warehouse.worker[0]
    worker_y = warehouse.worker[1]

    boxes = warehouse.boxes
    walls = warehouse.walls

    # Determine what kind of action it is and set the appropriate x and y
    x = 0
    y = 0
    xx = 0
    yy = 0
    if (action == "Up"):
        y -= 1
        yy -= 2
    elif (action == "Down"):
        y += 1
        yy += 2
    elif (action == "Left"):
        x -= 1
        xx -= 2
    elif (action == "Right"):
        x += 1
        xx += 2
    else:
        return False


    # checks if the worker's new coordinates is in a taboo place
    #checks if worker will push a box into a taboo place like a wall
    if (worker_x + x, worker_y + y) in walls:
        return False
    elif (worker_x + x, worker_y + y) in boxes and (worker_x + xx, worker_y + yy) in boxes:
        return False
    elif (worker_x + x, worker_y + y) in boxes and (worker_x + xx, worker_y + yy) in walls:
        return False
    else:
        return True

# can_go_there helper
class Pathing(search.Problem):

    #Tests to see if it is possible to get from A to B


    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.warehouse = warehouse

        self.goal = (goal[1], goal[0])

    def value(self, state):
        # move cost is = to 1
        moveCost = 1
        return moveCost

    def result(self, state, action):
        newX = state[0] + action[0]
        newY = state[1] + action[1]

        return newX, newY

    def actions(self, state):
        myTaboos = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for wall_Or_Box in myTaboos:
            stateWithWallorBox = state[0] + wall_Or_Box[0], state[1] + wall_Or_Box[1]

            if stateWithWallorBox not in self.warehouse.boxes and stateWithWallorBox not in self.warehouse.walls:
                yield wall_Or_Box


