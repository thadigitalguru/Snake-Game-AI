University of New England (UNE) - Trimester 2, 2023
# COSC550 Artificial Intelligence <br /> Practical Assignment 1


## Instructions 

This assignment requires you to implement the intelligent behaviour for the classic arcade game snake.

![A screenshot of the Snake game interface](https://github.com/KieranLH/UNE-550AI-A1/blob/main/example.png)

Snake is a classic arcade game where the player controls a growing snake (the green agent in the picture) on a bounded grid map. The objective is to eat food items (the red dots in the picture) that appear randomly on the screen, which causes the snake to grow longer and score points. The player must navigate the snake and avoid colliding with the boundaries of the play area, obstacles on the grid map (the white elements in the picture) or with its own body. The game continues until the snake collides with a boundary, an obstacle or itself, at which point the player's score is recorded. 

The goal of this assignment is to develop an artificial intelligence algorithm for an AI agent playing a timed version of the game of Snake, aiming to achieve a high score in the shorter time possible.

Important Note: A starter zip file containing the essential code to implement the game's graphical user interface (GUI) and logic has been provided. Please note that this assignment does not aim to assess your ability to develop the entire game. Instead, it focuses on evaluating your problem-solving skills in utilising AI techniques to implement the intelligent behaviour of the snake agent.

## Requirements:

Please, read the following requirements carefully as deviating from one or more of the requirements may lead to a score of 0.

1.  The program must be implemented by completing the Python template files provided in the starter zip. Please ensure to download the file from the link provided at the bottom of this page and strictly adhere to this guideline.
2.  The agent must be implemented with a Python class named *SnakeAgent* and inheriting from the base abstract class *Agent* available from the Python package une_ai illustrated during the workshops. An initial template for the class *SnakeAgent* is available in the file snake_agent.py provided in the starter zip. You should edit the snake_agent.py file, incorporating the necessary code to implement the agent. The parts of the template that should be completed by you are marked with comments.
3.  The *SnakeAgent* class must implement the following sensors with the available class methods illustrated during the workshops:
    *   *'body-sensor'*: it accepts a list of tuples, each one with 2 integer values being the x and y coordinates of a segment of the snake's body. The snake's head location is represented by the first tuple in the list, whereas the snake's tail is represented by the last tuple in the list;
    *   *'food-sensor'*: it accepts a list of tuples, each tuple having 3 integer values. The first two values are the map x and y coordinates of the food source and the third value is the score achieved when eating that food source. For example, the sensor value [(0, 3, 5), (10, 15, 2)] informs the agent that there are currently two food sources in the map, one at coordinates x=0 and y=3 worth 5 points and one at coordinates x=10 and y = 15 worth 2 points;
    *   *'obstacles-sensor'*: it accepts a list of tuples, each tuple having 2 integer values being the x coordinate and the y coordinate of the obstacle in the 2D grid map. Note that the coordinates of the snake's body are not included in this list;
    *   *'clock'*: it accepts the remaining time before the Game Over state, measured in seconds.
4.  The *SnakeAgent* class must implement the following actuators:
    *   *'head'.* The 'head' actuator accepts the string values 'up', 'down', 'left', and 'right'. It adjusts the snake's head trajectory according to the chosen direction, allowing it to continue in that trajectory until a new direction is selected;
    *   *'mouth'.* The 'mouth' actuator accepts the string values 'open' or 'close'. When the snake's mouth is open, it can consume the food located at its current position. Note that the snake moves first and then attempt to eat, therefore you may need to open the mouth just before ending up on a food coordinate (and close it afterward). If the snake tries to eat from an empty location, the player's score will incur a penalty .
5.  The *SnakeAgent* class must implement the following actions:
    *   *'move-up'* : this action changes the state of the 'head' actuator to the value 'up' if the current value for the 'head' actuator is not 'down';
    *   *'move-down'*:  this action changes the state of the 'head' actuator to the value 'down' if the current value for the 'head' actuator is not 'up';
    *   *'move-left'* : this action changes the state of the 'head' actuator to the value 'left' if the current value for the 'head' actuator is not 'right';
    *   *'move-right'* : this action changes the state of the 'head' actuator to the value 'right' if the current value for the 'head' actuator is not 'left';
    *   *'open-mouth'* : this action changes the state of the 'mouth' actuator to the value 'open';
    *   *'close-mouth'* : this action changes the state of the 'mouth' actuator to the value 'close'.
6. Implement the agent program by completing the function *snake_agent_program*  located in the file snake_agent_program.py within the starter zip. This function takes the current state's percepts and actuator values as inputs and should return a list of actions to be executed during that state. The objective of this function is to select actions that can maximise the game score in the shortest amount of time possible.\
    Please note:
    *   To incorporate intelligent behaviour into the agent's model, you have the freedom to employ any technique, data structure and algorithm covered in this unit so far (up to Week 4). However, it's crucial to prioritise efficient and optimised solutions, as they will be awarded higher scores compared to inefficient or overly simplistic approaches. While you can incorporate additional techniques and data structures that haven't been discussed in this unit so far, they need not be the core elements for achieving intelligent behaviour in the agent. While developing your code, you have the option to utilise code from lectures and workshops, but it is important to acknowledge the source by including comments. Additionally, ensure that your code functions properly without requiring the installation of any additional dependencies beyond those already included in the Python package une_ai and those available by default in the Python installation.
    *   It is not possible to perform more than one action from the set {'move-up', 'move-down', 'move-left', 'move-right'} and the set {'open-mouth', 'close-mouth'} during a single step of the game. Therefore, if more than one action in these sets is selected by the agent program during a single game step, only the last action in the list will take place. For example, if the actions selected by the agent program at time *t* are ['move-up', 'move-down', 'open-mouth', and 'close-mouth'], only the actions 'move-down' and 'close-mouth' will be carried out at time *t* .
    *   The snake cannot move to the opposite direction is currently moving. If this action is attempted during the game, it will generate an error. For example, if the head of the snake is currently set to 'up', the action 'move-down' is considered an illegal move (the snake must first turn left or right and then down). 
    *   The GridMap of the snake game environment is sized 64 x 48 (columns x rows).

7. Update the REPORT.md file to include a report detailing your problem solving and implementation process (max 500 words). The report must include the following information: 
    *   *Class of Agent Program* : Specify which class your implementation of the agent program falls into (simple-reflex, model-based, goal-based, utility-based), and explain why you believe your agent program can be classified under this particular class. 
    *   *AI Techniques Considered* : Discuss the AI techniques you considered to solve the problem. Explain which techniques you ultimately chose to implement and justify how your selection aligns with the objective of the agent. If you tested different solutions, you can mention the tests you performed to inform your final selection.
    *   *Reflections* : Describe the challenges you encountered during the problem-solving and implementation processes and outline how you tackled or attempted to overcome them. 

## Running and testing the code

To run and test the snake game simulation offered in the starter zip on Turing:

1.  Connect to Turing via X2go (to run this application you need a GUI, therefore, you cannot test the application with a ssh connection to Turing)
2.  Make sure to have the unzipped starter zip on the Turing machine (with your implementation if you are testing it)
3.  Open a terminal window on Turing
4.  In the terminal window activate the conda environment with the une_ai Python package installed, as demonstrated during the workshop on Week 1
5.  In the terminal window, using the Linux command cd access the folder that you extracted from the starter zip and that you adapted with your code
6.  Run the command: python3 snake_game.py
7.  If everything went well, you should be able to see the GUI of the game. If your code has errors, you may see the game's window closing and error messages displayed on the terminal window.

## Submission

To submit, please:

1.  Zip the entire directory with all the Python files from the starter zip with your changes
2.  Submit the zip file to Moodle  

Marking criteria
----------------

| Category | Weighting | Poor | Fair | Good |
| --- | --- | --- | --- | --- |
| Agent program implementation | /7 marks | The agent program is not implemented according to the specified requirements (E.g. it accesses information that the agent does not have access to, it changes the behaviour of the agent directly instead of returning a list of actions to perform during the current state, etc.). **0 marks** | The agent program is implemented according to the specified requirements but it is missing some crucial elements, contains bugs, the agent does not seem to exhibit an intelligent behaviour or the application is significantly slow due to heavy computations. **1-4 marks** | The agent program is fully implemented and the agent clearly exhibits an intelligent behaviour. The mark for this band is based on the final score achieved by the snake at timeout*: <br /><br /> Poor score (0 - 40): **5 marks** <br /><br /> Good score (41 - 80): **6 marks** <br /><br /> Excellent score (> 80): **7 marks** <br /><br /> *Note: as the score of the agent can vary due to the random generation of food in the game board, the offered thresholds are just indicative and borderline scores will be bumped up to the highest score. |
| Report (max 1 mark for each section of the report) | /3 marks | The report for the section in question fails to address the requirements adequately, lacks clarity, and contains significant inaccuracies. <br /><br /> **0 marks** | The report for the section in question partially addresses the requirements but it is hard to understand . While there is some attempt to convey the intended information, the overall presentation is imprecise, resulting in a limited understanding of the topic / question. <br /><br /> **0.5 marks** | The report for the section in question effectively addresses the requirements and provides a clear explanation of the topic / question. <br /><br /> **1 mark** |
