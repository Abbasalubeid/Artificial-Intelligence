The purpose with this lab is to introduce the agent paradigm. The goal is to program an agent to autonomously clean a randomly generated world of various sizes, potentially with obstacles. The agent's goal is to clean all dirty squares and return to its starting position.

## Task 1

Task 1 was to make the agent start from a random location, suck up all dirt in a rectangular world of unknown dimensions without obstacles, and shut down on the home position (home position can be sensed through one of the percepts). At the end the agent should also have a fully updated world model (i.e. world variable in MyAgentState).

1.	Agent visits all cells in a rectangular path, starting from the map’s outer edges and progressively visiting inner “subrectangles.”
2.	Initially, boundaries are set according to the map’s dimensions.
3.	Random starting position of the agent is corrected by placing it to the right of the home position, facing east.
4.	Upon start, the agent moves east until hitting the east boundary, then turns right, adjusting the boundary.
5.	The agent continues this pattern: moving forward, hitting boundaries, turning right, and adjusting boundaries accordingly.
6.	This process shrinks the boundaries inward until the agent reaches the center, having visited all cells.
7.	When the center is reached, the agent is directed to go home, moving north until hitting a wall, then turning left to reach the home position.

![](L1-task1.gif)



# Notes

The agent paradigm is a key concept in Artificial Intelligence (AI) that models systems as autonomous entities called agents. These agents perceive their environment, make decisions, and act to achieve specific objectives. They can operate independently, whether in dynamic, unpredictable environments or in more stable, predictable ones.

## Types of Agents

- **Simple reflex agents**: Act only on the current situation, ignoring the history of percepts. Example: A vacuum cleaner that sucks dirt when it's dirty and moves when it's clean.
- **Model-based reflex agents**: Keep track of their environment's history using a model of the world.
- **Goal-based agents**: Choose actions to achieve specific goals (like a self-driving car reaching a destination).
- **Utility-based agents**: Focuses not only on goals, but also on the best way to achieve them by maximizing performance or overall effectiveness


## Environments

1. **Fully observable vs. Partially observable**:

   - **Fully observable**: The agent can access all relevant information about the environment. For example, in chess, the agent can see the entire board and all the pieces.
   - **Partially observable**: The agent only has partial information. A taxi driver can’t see the exact movements of all other cars or predict weather conditions perfectly.

2. **Single-agent vs. Multi-agent**:

   - **Single-agent**: The agent is the only decision-making entity (e.g., a vacuum cleaner robot).
   - **Multi-agent**: Multiple agents interact. This can be **competitive** (e.g., chess, where one agent’s gain is another’s loss) or **cooperative** (e.g., cars driving on the road, where avoiding collisions benefits all agents).

3. **Deterministic vs. Nondeterministic (Stochastic)**:

   - **Deterministic**: The next state is fully determined by the current state and the agent's action. For example, a chess game is deterministic.
   - **Nondeterministic**: There is uncertainty, and actions may have multiple possible outcomes. Driving in traffic is nondeterministic, you can’t predict how other drivers will behave.

4. **Episodic vs. Sequential**:

   - **Episodic**: The agent's experience is divided into independent episodes. For example, image recognition software treats each image independently.
   - **Sequential**: Current decisions affect future decisions. For instance, in driving, every turn and brake affects the overall journey.

5. **Static vs. Dynamic**:

   - **Static**: The environment doesn’t change while the agent is deciding. A crossword puzzle is static.
   - **Dynamic**: The environment changes over time, and the agent has to keep up. Taxi driving is dynamic, as traffic and weather can change while the agent is deciding.

6. **Discrete vs. Continuous**:

   - **Discrete**: The environment has a finite number of distinct states. Chess is discrete because there are a fixed number of moves and pieces.
   - **Continuous**: The environment has a range of states, often including continuous values. Taxi driving is continuous because it involves varying speeds, distances, and steering angles.

7. **Known vs. Unknown**:
   - **Known**: The agent knows how the environment works (its rules). For example, chess has known rules.
   - **Unknown**: The agent has to learn or figure out the rules of the environment. A taxi driver in a foreign country may face unknown traffic laws or road conditions.

### PEAS Framework

When designing an agent, you need to define its **task environment**. The PEAS framework helps categorize the agent's environment:

- **P**erformance measure: How do we measure the success of the agent? For example, a taxi-driving agent might be evaluated on getting passengers to their destination safely and quickly.
- **E**nvironment: What does the world look like for this agent? For a taxi, it could be roads, traffic, pedestrians, weather, etc.
- **A**ctuators: What can the agent do? For a taxi, actuators include steering, brakes, accelerator, etc.
- **S**ensors: What can the agent sense? A taxi uses cameras, GPS, speedometers, etc.

### **Examples of Task Environments**

The PEAS framework is applied to different agents:

- **Taxi driver**: The agent needs to drive safely, considering other cars, road conditions, passengers, and traffic laws. The environment is dynamic, partially observable, and multi-agent.
- **Medical diagnosis system**: This agent helps in diagnosing diseases based on patient symptoms. It operates in a partially observable environment where the state of the patient is not fully known.


