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
    
    # Check if next tile is an obstacle 
    for p in obst_pos:
        if p[0] == new_x and p[1] == new_y:
            value = 'wall'
            
    # Check if next tile is food 
    for f in food_pos:
        if f[0] == new_x and f[1] == new_y:
            value = 'food'

    return value

def get_opp_dir(dir):
    """Return opposite of current direction (180°)."""
    opp_dir_index = DIRECTIONS.index(dir) + len(DIRECTIONS) // 2
    opp_dir_index %= len(DIRECTIONS)
    return DIRECTIONS[opp_dir_index]

def simple_reflex_behaviour(percepts, actuators, actions):
    cur_dir = actuators['head']
    body_pos = percepts['body-sensor']
    food_pos = percepts['food-sensor']
    obst_pos = percepts['obstacles-sensor']
    
    cur_dir = actuators['head']
    
    valid_turns = DIRECTIONS.copy()
    valid_turns.remove(get_opp_dir(cur_dir))
    
    new_dir = cur_dir
    while True:
        if next_tile(env_map, new_dir, body_pos, food_pos, obst_pos) != 'wall':
            break
        valid_turns.remove(new_dir)
        if len(valid_turns) == 0:
            break
        new_dir = random.choice(valid_turns)
    
    food = False
    for dir in valid_turns:
        if next_tile(env_map, dir, body_pos, food_pos, obst_pos) == 'food':
            new_dir = dir
            food = True
            break
    
    if food:
        actions.append('open-mouth')
    else:
        actions.append('close-mouth')

    if cur_dir != new_dir:
        actions.append('move-%s' %new_dir)
    
    return actions

def snake_agent_program(percepts, actuators):
    actions = []
    
    actions = simple_reflex_behaviour(percepts, actuators, actions)
    
    return actions