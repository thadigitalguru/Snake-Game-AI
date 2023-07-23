from une_ai.assignments.snake_game import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE
from une_ai.models import GridMap
from snake_agent import SnakeAgent

DIRECTIONS = SnakeAgent.DIRECTIONS

env_w = int(DISPLAY_WIDTH/ TILE_SIZE)
env_h = int(DISPLAY_HEIGHT/TILE_SIZE)
env_map = GridMap(env_w, env_h, None)

def initialise_env_map(percepts):
    global env_map

    if percepts['clock'] == 60:
        env_w = int(DISPLAY_WIDTH / TILE_SIZE)
        env_h = int(DISPLAY_HEIGHT / TILE_SIZE)
        env_map = GridMap(env_w, env_h, None)
        for i in percepts['obstacles-sensor']:
            env_map[i[1]][i[0]] = 'wall'
            
def snake_agent_program(percepts, actuators):
    # Perceive environment...
    
    # Setup variables
    actions = []
    cur_dir = actuators['head']
    new_dir = cur_dir
    body_pos = percepts['body-sensor']
    valid_dirs = DIRECTIONS.copy()
    valid_dirs.remove(cur_dir)
    next_tile = None
    max_utility = 0
    
    # Utility function to check if the next tile is safe (not a wall or body part)
    def is_safe_tile(x, y):
        return (
            0 <= x < env_w 
            and 0 <= y < env_h
            and (env_map.get_item_value(x,y) == None or 
                env_map.get_item_value(x,y) == 'food')
        )
    
    # Update body location on the map
    for x, y in body_pos:
        env_map.set_item_value(x, y, 'body')
    
    # Utility function to calculate the Manhattan distance between two positions
    def calculate_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    # UTILITY: Choose the best direction
    for dir in valid_dirs:
        dx, dy = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}[dir]
        new_head_x, new_head_y = body_pos[0][0] + dx, body_pos[0][1] + dy
        
        if is_safe_tile(new_head_x, new_head_y):
            # Get the utility value for this direction based on distance to food
            cur_utility = -calculate_distance((new_head_x, new_head_y), percepts['food-sensor'][0])
            # Record the highest scoring direction
            if cur_utility > max_utility:
                max_utility = cur_utility
                new_dir = dir
    
    # Use the best direction if it is different from the current direction
    if new_dir != cur_dir:
        actions.append('move-' + new_dir)
    
    # Finished thinking, act
    return actions
