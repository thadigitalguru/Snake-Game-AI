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
from snake_agent import SnakeAgent

DIRECTIONS = SnakeAgent.DIRECTIONS

"""
TODO:
You must implement this function with the
agent program for your snake agent.
Please, make sure that the code and implementation 
of your agent program reflects the requirements in
the assignment. Deviating from the requirements
may result to score a 0 mark in the
agent program criterion.

Please, do not change the parameters of this function.
"""
def snake_agent_program(percepts, actuators):
    actions = []
    
    # Choose a new random direction
    new_dir = random.choice(DIRECTIONS)
    actions.append('move-{0}'.format(new_dir))
    
    return actions