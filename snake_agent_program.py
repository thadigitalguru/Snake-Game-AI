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
SCORE_MODIFIER = 0.5

env_w = int(DISPLAY_WIDTH/ TILE_SIZE)
env_h = int(DISPLAY_HEIGHT/TILE_SIZE)
env_map = GridMap(env_w, env_h, None)
obstacles_initialised = False
refresh = True
path = None
path_pos = 0

def initialise_obstacles(model, percepts):
    for i in percepts['obstacles-sensor']:
        model.set_item_value(i[0], i[1], 'wall')

def update_food(model, all_food):
    # Check through current food
    for food in all_food:
        # Add food to map if new
        if model.get_item_value(food[0], food[1]) is None:
            model.set_item_value(food[0], food[1], 'food-%s' %food[2])

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

def get_offset(dir):
    offset = {
        'up'   :( 0, -1),
        'right':( 1,  0),
        'down' :( 0,  1),
        'left' :(-1,  0)
    }
    return offset[dir]

def get_dir(point_a, point_b):
    x_offset = point_b[0] - point_a[0]
    y_offset = point_b[1] - point_a[1]
    dir = {
        ( 0, -1): 'up',
        ( 1,  0):'right',
        ( 0,  1):'down',
        (-1,  0):'left'
    }
    return dir[x_offset, y_offset]

def get_neighbour(cur_pos, dir):
    offset = get_offset(dir)
    return (cur_pos[0] + offset[0], cur_pos[1] + offset[1])

def get_neighbour_value(model, cur_pos, dir):
    new_pos = get_neighbour(cur_pos, dir)
    
    # check if next tile would be off the map
    try:
        value = model.get_item_value(new_pos[0], new_pos[1])
    except:
        value = 'wall'
    
    return (value, new_pos[0], new_pos[1])

def get_opp_dir(dir):
    """Return opposite of current direction (180°)."""
    opp_dir_index = DIRECTIONS.index(dir) + len(DIRECTIONS) // 2
    opp_dir_index %= len(DIRECTIONS)
    return DIRECTIONS[opp_dir_index]

def get_Manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def dist_heuristic_utility(cur_pos, food):
    max_dist = max(env_h, env_w)
    dist = get_Manhattan_distance(cur_pos, food)
    score = food[2]
    return max_dist - dist + score

def adjust_food_scores(in_food):
    out_food = []
    for food in in_food:
        out_food.append((food[0], food[1], round(food[2] * SCORE_MODIFIER)))
    return out_food

def sort_food(cur_pos, in_food):
    if in_food is None or len(in_food) == 0:
        return None
    tmp_food = in_food.copy()
    out_food = []
    while tmp_food:
        max_utility = MAX_UTILITY * -1
        best_food = None
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

def best_path(model, cur_pos, cur_dir, all_food):
    best_path = None
    best_food = all_food[0]

    def utility(path, food):
        return MAX_UTILITY - len(path) +  food[2]

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
            cur_dir = get_dir(parents[current], current)
        
        range_of_motion = DIRECTIONS.copy()
        range_of_motion.remove(get_opp_dir(cur_dir))
        
        # All possible directions from the current position are considered.
        for dir in range_of_motion:
            # The neighbour is the position resulting from 
            # taking an action from the current position.
            neighbour = get_neighbour(current, dir)
            # If the neighbour position has not been explored and is not a wall,
            # it is considered for exploration.
            if (neighbour not in explored and 
                neighbour not in model.find_value('wall') and
                neighbour not in model.find_value('body')):
                
                # The new_cost to reach the neighbour is the cost to reach 
                # the current position plus the cost to move from the 
                # current position to the neighbour.
                new_cost = g_score[current] + 1
                # If the neighbour has not been considered before, 
                # or a cheaper path to the neighbour has been found, 
                # the cost to reach the neighbour 
                # and its parent position are updated.
                if neighbour not in g_score or new_cost < g_score[neighbour]:
                    g_score[neighbour] = new_cost
                    # The priority of the neighbour is the cost to reach it 
                    # plus the estimated cost to reach the goal from there.
                    priority = new_cost + heuristic(neighbour)
                    heapq.heappush(frontier, (priority, neighbour))
                    parents[neighbour] = current
    # Open set is empty but goal was never reached
    return None

def obstacle_reflex(model, head_pos, cur_dir, valid_dirs):
    new_dir = cur_dir
    # REFLEX: avoid obstacles
    while True:
        # Check if next tile is safe (not a wall or body part)
        next_tile = get_neighbour_value(model, head_pos, new_dir)
        if next_tile[0] not in ['wall', 'body']:
            # Safe
            break
        # Dangerous, avoid
        print('REFLEX: %s is a %s. Avoiding...' %(new_dir, next_tile[0]))
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

def mouth_reflex(actions, env_map, new_dir, head_pos, actuators):
    global refresh
    
    # REFLEX: Open/close mouth for food
    next_tile = get_neighbour_value(env_map, head_pos, new_dir)
    # Check if next tile is food
    if next_tile[0] != None and next_tile[0].startswith('food'):
        # Incoming food. Open mouth
        actions.append('open-mouth')
        # DEBUGGING: Print eaten food's score
        map_tile = env_map.get_item_value(next_tile[1], next_tile[2])
        _, score = map_tile.split('-')
        # Remove food from map
        env_map.set_item_value(next_tile[1], next_tile[2], None)
        # Refresh on next cycle
        refresh = True
    # Check if mouth is open
    elif actuators['mouth'] == 'open':
        # No food & open mouth. Close mouth
        actions.append('close-mouth')

def snake_agent_program(percepts, actuators):
    global refresh
    global path
    global path_pos
    
    # Setup variables
    actions = []
    body = percepts['body-sensor']
    head_pos = body[0]
    all_food = percepts['food-sensor']
    cur_dir = actuators['head']
    new_dir = cur_dir
    safe_dirs = DIRECTIONS.copy()
    safe_dirs.remove(get_opp_dir(cur_dir))
    
    # obstacle location setup (only once at launch)
    if percepts['clock'] == 60:
        initialise_obstacles(env_map, percepts)
    
    if refresh:
        # Adjust food scores and sort by heuristic utility
        all_food = adjust_food_scores(all_food)
        all_food = sort_food(head_pos, all_food)
        
        # Update new food and body locations
        update_food(env_map, all_food)
        update_body(env_map, body.copy())
    
        # Use A* algorithm to the find the best path to best food
        path = best_path(env_map, head_pos, cur_dir, all_food)
        
        # Finished refreshing
        refresh = False
        path_pos = 0
    
    if path and len(path) >= 2 and path_pos < len(path):
        new_dir = get_dir(path[path_pos], path[path_pos + 1])
        path_pos += 1
    
    # Safety redundancy, reflex away from a crash course
    new_dir = obstacle_reflex(env_map, head_pos, new_dir, safe_dirs)
    
    # reflexively open and close mouth for food
    mouth_reflex(actions, env_map, new_dir, head_pos, actuators)
    
    # Update direction if necessary
    if new_dir != cur_dir:
        actions.append('move-%s' %new_dir)
    
    return actions