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

def initialise_obstacles(percepts):
    for i in percepts['obstacles-sensor']:
        env_map.set_item_value(i[0], i[1], 'wall')
    setup_map = True

def update_map(percepts):
    # Populate obstacles locations
    if not obstacles_initialised:
        initialise_obstacles(percepts)
    
    # Update food locations
    for f in percepts['food-sensor']:
        if env_map.get_item_value(f[0], f[1]) != 'food':
            env_map.set_item_value(f[0], f[1], 'food')

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
    dist_penalty = 0
    # search from closest to furthest
    for tile in visible_tiles:
        if tile == 'food':
            # food found! Return calculate utility
            return reward - dist_penalty
        # Nothing yet. Add to the distance penalty counter, continue
        dist_penalty += 1
    
    # No food found. Return no utility
    return 0

def snake_agent_program(percepts, actuators):
    
    # Update game environment
    update_map(percepts)
    
    # initiate variables
    actions = []
    cur_dir = actuators['head']
    new_dir = cur_dir
    body_pos = percepts['body-sensor']
    valid_turns = DIRECTIONS.copy()
    valid_turns.remove(get_opp_dir(cur_dir))
    next_tile = None
    max_utility = 0
    
    # Reflexively avoid obstacle
    while True:
        next_tile = get_next_tile(env_map, new_dir, body_pos)
        if next_tile[0] not in ['wall', 'body']:
            break
        print('%s %s' %(next_tile[0], new_dir))
        valid_turns.remove(new_dir)
        if len(valid_turns) == 0:
            print('FAIL: No more valid turns to choose from!')
            break
        new_dir = random.choice(valid_turns)
    
    # Utility maximise direction
    print('before for loop: %s' %new_dir)
    for dir in valid_turns:
        cur_utility = calculate_utility(env_map, body_pos[0], dir)
        print('%s utility is %d' %(dir, cur_utility))
        if cur_utility > max_utility:
            max_utility = cur_utility
            new_dir = dir
    
    # Reflexively open/close mouth for food
    next_tile = get_next_tile(env_map, new_dir, body_pos)
    if next_tile[0] is 'food':
        actions.append('open-mouth')
        env_map.set_item_value(next_tile[1], next_tile[2], None)
    elif actuators['mouth'] == 'open':
        actions.append('close-mouth')
    
    # Change direction if better found
    if new_dir != cur_dir:
        actions.append('move-%s' %new_dir)
    
    return actions