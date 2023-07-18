""" University of New England (UNE)
COSC550 Artificial Intelligence (T2 2023) - Practical Assignment 1
Kieran Hillier - Student ID: 220281036
"""

import random
import numpy as np
from une_ai.assignments.snake_game import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE
from une_ai.models import GridMap
from snake_agent import SnakeAgent

DIRECTIONS = SnakeAgent.DIRECTIONS

env_w = int(DISPLAY_WIDTH/ TILE_SIZE)
env_h = int(DISPLAY_HEIGHT/TILE_SIZE)
env_map = GridMap(env_w, env_h, None)
obstacles_initialised = False

def initialise_obstacles(percepts, model):
    for i in percepts['obstacles-sensor']:
        model.set_item_value(i[0], i[1], 'wall')

def update_food(percepts, model):    
    # Check through current food...
    for cur_f in percepts['food-sensor']:
        # Add food to map if new
        if model.get_item_value(cur_f[0], cur_f[1]) is None:
            model.set_item_value(cur_f[0], cur_f[1], 'food-%s' %cur_f[2])

def get_next_tile(model, direction, body_pos):
    offset = {
        'up'   :( 0, -1),
        'right':( 1,  0),
        'down' :( 0,  1),
        'left' :(-1,  0)
    }
    head_x, head_y = body_pos[0]
    new_x, new_y = (head_x + offset[direction][0], head_y + offset[direction][1])
    
    try:
        value = model.get_item_value(new_x, new_y)
    except:
        value = 'wall'
    
    for b in body_pos:
        if b[0] == new_x and b[1] == new_y:
            value = 'body'
    
    return (value, new_x, new_y)

def get_opp_dir(dir):
    """Return opposite of current direction (180°)."""
    opp_dir_index = DIRECTIONS.index(dir) + len(DIRECTIONS) // 2
    opp_dir_index %= len(DIRECTIONS)
    return DIRECTIONS[opp_dir_index]

def calculate_utility(model, cur_pos, direction):
    x, y = cur_pos
    # get all cells in given direction
    if direction == 'up':
        tiles = model.get_column(x)
        tiles = np.flip(tiles[0:y])
    elif direction == 'down':
        tiles = model.get_column(x)
        tiles = tiles[y+1:]
    elif direction == 'left':
        tiles = model.get_row(y)
        tiles = np.flip(tiles[0:x])
    elif direction == 'right':
        tiles = model.get_row(y)
        tiles = tiles[x+1:]
    else:
        tiles = []
    
    # remove cells obstructed by an obstacle
    visible_tiles = []
    for tile in tiles:
        if tile != 'wall':
            visible_tiles.append(tile)
        else:
            # wall
            break
    
    # check if, and how far away food is in that direction
    max_dist = max(env_h, env_w)
    reward = max_dist
    score = 0
    dist_penalty = 0
    # search from closest to furthest
    for tile in visible_tiles:
        if tile != None and tile.startswith('food'):
            # food found! Extract its score
            _, score = tile.split('-')
            score = int(score)
            # Calculate and return utility value
            return reward + score - dist_penalty
        # Nothing yet. Add to the distance penalty counter, continue
        dist_penalty += 1
    
    # No food found. Return no utility
    return 0

def snake_agent_program(percepts, actuators):
    
    # Perceive environment...
    
    # Setup variables
    actions = []
    cur_dir = actuators['head']
    new_dir = cur_dir
    body_pos = percepts['body-sensor']
    valid_dirs = DIRECTIONS.copy()
    valid_dirs.remove(get_opp_dir(cur_dir))
    next_tile = None
    max_utility = 0
    
    # Add obstacles only once
    if percepts['clock'] == 60:
        initialise_obstacles(percepts, env_map)
    
    # Add any new food
    update_food(percepts, env_map)
    
    # REFLEX: avoid obstacles
    while True:
        # Check if next tile is safe (not a wall or body part)
        next_tile = get_next_tile(env_map, new_dir, body_pos)
        if next_tile[0] not in ['wall', 'body']:
            # Safe
            break
        # Dangerous, avoid
        print('%s is a %s' %(new_dir, next_tile[0]))
        # Remove direction from list of valid choices
        valid_dirs.remove(new_dir)
        # Check if there are any remaining directions to try
        if len(valid_dirs) == 0:
            # Dead-end, all directions are dangerous. No more directions to try
            print('FAIL: No more valid turns to choose from!')
            break
        # More directions to try, pick one at random
        new_dir = random.choice(valid_dirs)
    
    # UTILITY: Choose the best direction
    for dir in valid_dirs:
        # Get the utility value for this direction
        cur_utility = calculate_utility(env_map, body_pos[0], dir)
        # Record the highest scoring direction
        if cur_utility > max_utility:
            if dir != new_dir:
                print('%s(%d) is beter than %s(%d)' 
                    %(dir, cur_utility, new_dir, max_utility))
            max_utility = cur_utility
            new_dir = dir
    
    # REFLEX: Open/close mouth for food
    next_tile = get_next_tile(env_map, new_dir, body_pos)
    if next_tile[0] != None and next_tile[0].startswith('food'):
        # Food! Open mouth
        actions.append('open-mouth')
        # DEBUGGING: Print eaten food's score
        map_tile = env_map.get_item_value(next_tile[1], next_tile[2])
        _, score = map_tile.split('-')
        print('food eaten! +%s points' %score)
        # Remove food from map
        env_map.set_item_value(next_tile[1], next_tile[2], None)
    # No food. Close mouth
    elif actuators['mouth'] == 'open':
        actions.append('close-mouth')
    
    # Move, if better direction
    if new_dir != cur_dir:
        actions.append('move-%s' %new_dir)
        print('Moving %s' %new_dir)
    
    # Finished thinking, act
    return actions