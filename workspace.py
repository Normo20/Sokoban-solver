# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:02:35 2020

@author: User
"""

import search 
import sokoban


wh = sokoban.Warehouse()
wh.load_warehouse("./warehouses/warehouse_03.txt")
print(wh)
dst= (1, 1)




def find_size(wh):
    '''
    Helper function in order to find the size of the warehouse
    Both x and y axis
   input warehouse:
    
    returns
   x_size:  the column size of warehouse
   y_size: the row size of warehouse
    '''
    
    # Determine the y size of the warehouse by splitting all '\n'
    cells = str(wh).split('\n')    
    
    # Split all the strings into individual characters in order to determine 
    # the x size
    index = 0
    for strings in cells:
        cells[index] = list(strings)
        index += 1

    # Add +1 because lists starts with 0
    x_size = len(cells[0])
    y_size = len(cells)

    
    return (x_size, y_size)



#--------------------------------------------------------------------------------------------------------------------------



size_x, size_y = find_size(wh)
    
    # Set worker's x and y coordinates
worker_x = wh.worker[0]
worker_y = wh.worker[1]
    
    # Set destination's x and y coordinates
dst_x = dst[0]
dst_y = dst[1]
    
for box in wh.boxes:
        # Set boxes' x and y coordinates
        box_x = box[0]
        box_y = box[1]
        
        # The worker cannot move to the destination:
        # If the box is on top of the destination
        # Or if the box is between the destination and worker in x coordinates
        # Or if the box is between the destination and worker in y coordinates
        # Or if the destination is out of bound (double elif statements)
        if box == dst:
            a= False
            print(a)
        elif box_x in range(worker_x, dst_x) and box_y == worker_y: 
            a= False      
            print(a)
        elif box_y in range(worker_y, dst_y) and box_x == worker_x:
            a= False
            print(a)
        elif dst_x <= 0 or dst_x > size_x:
            a= False
            print(a)
        elif dst_y <= 0 or dst_y > size_y:
            a= False
            print(a)
    
a= True
print(a)
print(worker_x,worker_y)