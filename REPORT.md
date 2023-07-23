**Kieran Hillier** - 220281036 | UNE COSC550 Artificial Intelligence (T2 2023)
 
# Practical Assignment 1 Report

### Class of Agent Program

My implementation falls under the class of utility-based agents. While it possesses some reflex characteristics, the agent primarily uses a model of the environment and calculates the utility of each food item based on its score and path distance. This enables it to determine an optimal course of action, justifying its classification as a utility-based agent.

### AI Techniques Considered
Initially, I attempted a simple line-of-sight utility function, inspired by the week two workshop. However, the performance was poor, leading me to consider more advanced techniques. I finally decided on an A* search algorithm paired with a utility function for my agent. This approach prioritises closer, high-value food items, aligning directly with the agent's objective of maximizing its score in a limited time.

### Reflections
The assignment presented a steep learning curve for me. Implementing an effective utility-based agent proved initially challenging but familarised me with how the agent works. I was interested in whether I could implement a pathfinding algorithm. searching online, I found the A* search algorithm but implementing it was a significant challenge, only overcome through extensive debugging and refinement. This iterative process not only enhanced the performance of my agent but also enriched my understanding of AI techniques and problem-solving methodologies.
