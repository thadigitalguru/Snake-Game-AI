""" University of New England (UNE)
COSC550 Artificial Intelligence (T2 2023) - Practical Assignment 1
Kieran Hillier - Student ID: 220281036
"""

import heapq
import random
import numpy as np
from collections import defaultdict
from une_ai.assignments.snake_game import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE
from une_ai.models import GridMap
from snake_agent import SnakeAgent

DIRECTIONS = SnakeAgent.DIRECTIONS
MAX_UTILITY = 1000

env_w = int(DISPLAY_WIDTH/ TILE_SIZE)
env_h = int(DISPLAY_HEIGHT/TILE_SIZE)
env_map = GridMap(env_w, env_h, None)
obstacles_initialised = False

def initialise_obstacles(model, percepts):
    for i in percepts['obstacles-sensor']:
        model.set_item_value(i[0], i[1], 'wall')

def update_food(model, percepts):
    # Check through current food
    for cur_f in percepts['food-sensor']:
        # Add food to map if new
        if model.get_item_value(cur_f[0], cur_f[1]) is None:
            model.set_item_value(cur_f[0], cur_f[1], 'food-%s' %cur_f[2])

def update_body(model, body):
    # Remove all body previous locations
    for b in model.find_value('body'):
        model.set_item_value(b[0], b[1], None)
    
    # Add all but the last body part to  map
    # (the tail will move out of the way in the next turn)
    del body[-1]
    # Add remaining to map
    for b in body:
        model.set_item_value(b[0], b[1], 'body')

def dir_to_offset(dir):
    offset = {
        'up'   :( 0, -1),
        'right':( 1,  0),
        'down' :( 0,  1),
        'left' :(-1,  0)
    }
    return offset[dir]

def offset_to_dir(offset):
    dir = {
        ( 0, -1): 'up',
        ( 1,  0):'right',
        ( 0,  1):'down',
        (-1,  0):'left'
    }
    return dir[offset]

def get_dir(point_a, point_b):
    x_offset = point_a[0] - point_b[0]
    y_offset = point_a[1] - point_b[1]
    dir = {
        ( 0, -1): 'up',
        ( 1,  0):'right',
        ( 0,  1):'down',
        (-1,  0):'left'
    }
    return dir[x_offset, y_offset]

def get_next_tile(model, dir, body_pos):
    offset = {
        'up'   :( 0, -1),
        'right':( 1,  0),
        'down' :( 0,  1),
        'left' :(-1,  0)
    }
    head_x, head_y = body_pos[0]
    new_x, new_y = (head_x + offset[dir][0], head_y + offset[dir][1])
    
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

def get_Manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def dist_heuristic_utility(cur_pos, food):
    max_dist = max(env_h, env_w)
    dist = get_Manhattan_distance(cur_pos, food)
    score = food[2]
    return max_dist - dist + score

def sort_food(cur_pos, in_food):
    if in_food is None or len(in_food) == 0:
        return None
    tmp_food = in_food.copy()
    out_food = []
    while tmp_food:
        max_utility = 0
        best_food = ()
        if len(tmp_food) == 1:
            best_food = tmp_food[0]
        else:
            for food in tmp_food:
                utility = dist_heuristic_utility(cur_pos, food)
                if utility > max_utility:
                    max_utility = utility
                    best_food = food
        tmp_food.remove(best_food)
        out_food.append(best_food)
    return out_food

def path_utility(dist, score):
    return MAX_UTILITY - dist + score

def best_path(model, cur_pos, cur_dir, all_food):
    best_path = None
    best_food = all_food[0]

    def utility(path, food):
        return path_utility(len(path), food[2])

    for cur_food in all_food:
        # Get the path for the current food
        # cur_path = a_star_search(model, cur_pos, cur_food)

        head_x, head_y = cur_pos
        goal_x, goal_y, _ = cur_food
        cur_path = astar_search(env_map, cur_pos, cur_dir, cur_food, best_food, best_path)
        if cur_path is None:
            continue
        # Record the lowest scoring path
        if (best_path is None 
            or utility(cur_path, cur_food) > utility(best_path, best_food)):
            best_path = cur_path
            best_food = cur_food

    return best_path

def astar_search(model, head_pos, cur_dir, cur_food, best_food=None, best_path=None):
    start = (head_pos[0], head_pos[1])
    goal = (cur_food[0], cur_food[1])
    goal_score = cur_food[2]
    cur_path_cost = 0
    best_path_cost = None
    
    if best_food and best_path:
        best_path_cost = len(best_path) - best_food[2]
    
    
    # The heuristic function estimates the cost to reach the goal from start.
    # This implementation uses the Manhattan distance as a heuristic
    def heuristic(pos):
        return get_Manhattan_distance(pos, goal)
    
    def path_len(current, parents):
        length = 0
        while current in parents:
            current = parents[current]
            length += 1
        return length  # Return the length of current path
    
    # The frontier is a priority queue of positions yet to be explored.
    # This is determined by the cost to reach that position 
    # and the estimated cost to reach the goal from there.
    frontier = [(0, start)]
    # The explored set keeps track of positions that have already been explored.
    explored = set()
    # The dictionary 'g_score' maps a position its cost to reach from start.
    g_score = {start: 0}
    # The dictionary 'parents' maps a position to the previous position
    # from which it was reached.
    parents = defaultdict(lambda: None)

    # Loop as long as there are positions yet to be explored in the frontier.
    while frontier:
        # The position with the lowest priority is removed from the frontier 
        # and becomes the current position.
        _, current = heapq.heappop(frontier)
        
        # If current position is the goal, 
        # the path from the start to the goal has been found!
        if current == goal:
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            path.reverse()
            return path  # Return the found path
        
        # Check previous best path is better
        if parents is not None and best_path_cost is not None:
            cur_path_cost = path_len(current, parents) - goal_score
            if cur_path_cost >= best_path_cost:
                # Previous path is better. Give up searching
                return None
        
        # The current position is added to the set of explored positions.
        explored.add(current)
        
        # get the current direction the head will be facing
        if parents is not None and parents[current] is not None:
            previous = parents[current]
            offset = (previous[0] - current[0], previous[1] - current[1])
            cur_dir = offset_to_dir(offset)
        
        range_of_motion = DIRECTIONS.copy()
        range_of_motion.remove(get_opp_dir(cur_dir))
        
        # All possible directions from the current position are considered.
        for dir in range_of_motion:
            action = dir_to_offset(dir)
            # The neighbor is the position resulting from 
            # taking an action from the current position.
            neighbor = (current[0] + action[0], current[1] + action[1])
            # If the neighbor position has not been explored and is not a wall,
            # it is considered for exploration.
            if (neighbor not in explored and 
                neighbor not in model.find_value('wall') and
                neighbor not in model.find_value('body')):
                
                # The new_cost to reach the neighbor is the cost to reach 
                # the current position plus the cost to move from the 
                # current position to the neighbor.
                new_cost = g_score[current] + 1
                # If the neighbor has not been considered before, 
                # or a cheaper path to the neighbor has been found, 
                # the cost to reach the neighbor 
                # and its parent position are updated.
                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    # The priority of the neighbor is the cost to reach it 
                    # plus the estimated cost to reach the goal from there.
                    priority = new_cost + heuristic(neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    parents[neighbor] = current
    # Open set is empty but goal was never reached
    return None

def obstacle_reflex(model, body_pos, cur_dir, valid_dirs):
    new_dir = cur_dir
    # REFLEX: avoid obstacles
    while True:
        # Check if next tile is safe (not a wall or body part)
        next_tile = get_next_tile(model, new_dir, body_pos)
        if next_tile[0] not in ['wall', 'body']:
            # Safe
            break
        # Dangerous, avoid
        print('%s is a %s' %(new_dir, next_tile[0]))
        # Remove direction from list of valid choices
        if new_dir in valid_dirs:
            valid_dirs.remove(new_dir)
        # Check if there are any remaining directions to try
        if len(valid_dirs) == 0:
            # Dead-end, all directions are dangerous. No more directions to try
            print('FAIL: No more valid turns to choose from!')
            break
        # More directions to try, pick one at random
        new_dir = random.choice(valid_dirs)
    return new_dir

def mouth_reflex(actions, env_map, new_dir, body, actuators):
    # REFLEX: Open/close mouth for food
    next_tile = get_next_tile(env_map, new_dir, body)
    # Check if next tile is food
    if next_tile[0] != None and next_tile[0].startswith('food'):
        # Incoming food. Open mouth
        actions.append('open-mouth')
        # DEBUGGING: Print eaten food's score
        map_tile = env_map.get_item_value(next_tile[1], next_tile[2])
        _, score = map_tile.split('-')
        print('food eaten! +%s points' %score)
        # Remove food from map
        env_map.set_item_value(next_tile[1], next_tile[2], None)
    # Check if mouth is open
    elif actuators['mouth'] == 'open':
        # No food & open mouth. Close mouth
        actions.append('close-mouth')

def snake_agent_program(percepts, actuators):
    
    # Perceive environment...
    # Setup variables
    actions = []
    body = percepts['body-sensor']
    head_pos = body[0]
    all_food = sort_food(head_pos, percepts['food-sensor'])
    cur_dir = actuators['head']
    new_dir = cur_dir
    safe_dirs = DIRECTIONS.copy()
    safe_dirs.remove(get_opp_dir(cur_dir))
    
    # One-time setup
    if percepts['clock'] == 60:
        initialise_obstacles(env_map, percepts)
    
    # Add any new food
    update_food(env_map, percepts)
    # Update body location
    update_body(env_map, body.copy())
    
    """ Previous x, y line-of-sight utility
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
    """
    
    # Use A* algorithm to find the best path to food
    path = best_path(env_map, head_pos, cur_dir, all_food)

    if path and len(path) >= 2:
        next_x, next_y = path[1]
        if next_x == head_pos[0]:
            if next_y < head_pos[1]:
                new_dir = 'up'
            else:
                new_dir = 'down'
        elif next_y == head_pos[1]:
            if next_x < head_pos[0]:
                new_dir = 'left'
            else:
                new_dir = 'right'
    
    new_dir = obstacle_reflex(env_map, body, new_dir, safe_dirs)
    
    mouth_reflex(actions, env_map, new_dir, body, actuators)
    
    # Move, if better direction
    if new_dir != cur_dir:
        actions.append('move-%s' %new_dir)
        # print('Moving %s' %new_dir)
    
    # Finished thinking, act
    return actions