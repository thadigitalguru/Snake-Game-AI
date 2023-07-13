from une_ai.models import Agent

class SnakeAgent(Agent):

    # DO NOT CHANGE THE PARAMETERS OF THIS METHOD
    def __init__(self, agent_program):
        # DO NOT CHANGE THE FOLLOWING LINES OF CODE
        super().__init__("Snake Agent", agent_program)

        """
        If you need to add more instructions
        in the constructor, you can add them here
        """

    """
    TODO:
    In order for the agent to gain access to all 
    the sensors specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single sensor with the method:
    self.add_sensor(sensor_name, initial_value, validation_function)
    """
    def add_all_sensors(self):
        pass

    """
    TODO:
    In order for the agent to gain access to all 
    the actuators specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single actuator with the method:
    self.add_actuator(actuator_name, initial_value, validation_function)
    """
    def add_all_actuators(self):
        pass

    """
    TODO:
    In order for the agent to gain access to all 
    the actions specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single action with the method:
    self.add_action(action_name, action_function)
    """
    def add_all_actions(self):
        pass




