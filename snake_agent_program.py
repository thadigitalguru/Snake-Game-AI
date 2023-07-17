""" 
University of New England (UNE)
T2 2023 - COSC550 Artificial Intelligence - Practical Assignment 1
Kieran Hillier - Student ID: 220281036
"""

"""
You can import modules if you need
NOTE:
your code must function properly without 
requiring the installation of any additional 
dependencies beyond those already included in 
the Python package une_ai
"""
# import ...

# Here you can create additional functions
# you may need to use in the agent program function
import random
import logging
from une_ai.assignments.snake_game import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE
from une_ai.models import GridMap
from snake_agent import SnakeAgent

DIRECTIONS = SnakeAgent.DIRECTIONS
TILE_TYPE = ['wall', 'food', 'body']

env_w = int(DISPLAY_WIDTH/ TILE_SIZE)
env_h = int(DISPLAY_HEIGHT/TILE_SIZE)
env_map = GridMap(env_w, env_h, None)

def next_tile(model, direction, body_pos, food_pos, obst_pos):
    offset = {
        'up'   :( 0, -1),
        'right':( 1,  0),
        'down' :( 0,  1),
        'left' :(-1,  0)
    }
    head_x, head_y = body_pos[0]
    new_x, new_y = (head_x + offset[direction][0], head_y + offset[direction][1])

    # Check if next tile is off the map
    try:
        value = model.get_item_value(new_x, new_y)
    except:
        value = 'wall'
    
    # Check if next tile obstacle 
    for p in obst_pos:
        if p[0] == new_x and p[1] == new_y:
            value = 'wall'

    return value

def snake_agent_program(percepts, actuators):
    actions = []
    
    body_pos = percepts['body-sensor']
    food_pos = percepts['food-sensor']
    obst_pos = percepts['obstacles-sensor']
    
    
    #while True:
    for dir in DIRECTIONS:
        if next_tile(env_map, dir, body_pos, food_pos, obst_pos) != 'wall':
            actions.append('move-%s' %dir)
            break
    
    return actions