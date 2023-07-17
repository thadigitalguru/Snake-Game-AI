""" 
University of New England (UNE)
T2 2023 - COSC550 Artificial Intelligence - Practical Assignment 1
Kieran Hillier - Student ID: 220281036
"""

import numpy
from une_ai.models import Agent

class SnakeAgent(Agent):
    
    DIRECTIONS = ['up', 'right', 'down', 'left']

    def __init__(self, agent_program):
        super().__init__("Snake Agent", agent_program)

    def add_all_sensors(self):
        """Add sensors for the agent to perceive the environment."""
        # list of x,y int tuples coordinates for each body segment. 
        # Head is first, Tail is last.
        self.add_sensor('body-sensor', [(0,0)], lambda v:
                        isinstance(v,list) and 
                        len(v) > 0 and 
                        isinstance(v[0],tuple) and
                        isinstance(v[0][0],int) and 
                        isinstance(v[0][1],int))
        
        # list of x,y,score int tuples coordinates and score for each food.
        self.add_sensor('food-sensor', [(0,0,0)], lambda v:
                        isinstance(v,list) and 
                        len(v) > 0 and 
                        isinstance(v[0],tuple) and
                        isinstance(v[0][0],int) and 
                        isinstance(v[0][1],int) and 
                        (isinstance(v[0][2],int) or
                        isinstance(v[0][2],numpy.int32)))
        
        # list of x,y int tuples coordinates for each obstacle.
        self.add_sensor('obstacles-sensor', [(0,0)], lambda v:
                        isinstance(v,list) and 
                        len(v) > 0 and 
                        isinstance(v[0],tuple) and
                        isinstance(v[0][0],int) and 
                        isinstance(v[0][1],int))
        
        # Seconds remaining before the Game-Over state.
        self.add_sensor('clock', 0, lambda v: 
                        isinstance(v,int) and 
                        v >= 0)

    def add_all_actuators(self):
        """Add actuators for the agent to interact with the environment."""
        # Current direction the snake is facing and will travel
        self.add_actuator('head', 'up', lambda v: v in self.DIRECTIONS)
        
        # Current state of mouth (effects ability to eat).
        self.add_actuator('mouth', 'close', lambda v: v in ['open', 'close'])

    def add_all_actions(self):
        """Add actions for the agent to change it's state """
        # Change direction of head, max 90° in either direction.
        for dir in self.DIRECTIONS:
            self.add_action('move-%s' %dir, lambda: 
                            {'head': dir} if dir != self.get_opp_dir()
                            else {}
            )
        # Open/close mouth
        self.add_action('open-mouth',  lambda: {'mouth': 'open'})
        self.add_action('close-mouth', lambda: {'mouth': 'close'})
    
    def get_opp_dir(self):
        """Return opposite of current direction (180°)."""
        # get currently faced direction
        cur_dir = self.read_actuator_value('head')
        # get index of direction within DIRECTIONS list constant
        cur_dir_index = self.DIRECTIONS.index(cur_dir)
        # get opposite index, i.e. half way around the list
        opp_dir_index = cur_dir_index + int((len(self.DIRECTIONS) / 2) )
        opp_dir_index %= len(self.DIRECTIONS)
        # Return value at the opposite index
        return self.DIRECTIONS[opp_dir_index]