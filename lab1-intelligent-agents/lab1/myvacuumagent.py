from lab1.liuvacuum import *
from collections import deque

DEBUG_OPT_DENSEWORLDMAP = False

AGENT_STATE_UNKNOWN = 0
AGENT_STATE_WALL = 1
AGENT_STATE_CLEAR = 2
AGENT_STATE_DIRT = 3
AGENT_STATE_HOME = 4

AGENT_DIRECTION_NORTH = 0
AGENT_DIRECTION_EAST = 1
AGENT_DIRECTION_SOUTH = 2
AGENT_DIRECTION_WEST = 3

def direction_to_string(cdr):
    cdr %= 4
    return  "NORTH" if cdr == AGENT_DIRECTION_NORTH else\
            "EAST"  if cdr == AGENT_DIRECTION_EAST else\
            "SOUTH" if cdr == AGENT_DIRECTION_SOUTH else\
            "WEST" #if dir == AGENT_DIRECTION_WEST

"""
Internal state of a vacuum agent
"""
class MyAgentState:

    def __init__(self, width, height):

        # Initialize perceived world state
        self.world = [[AGENT_STATE_UNKNOWN for _ in range(height)] for _ in range(width)]
        self.world[1][1] = AGENT_STATE_HOME

        # Agent internal state
        self.last_action = ACTION_NOP
        self.direction = AGENT_DIRECTION_EAST
        self.pos_x = 1
        self.pos_y = 1

        # Metadata
        self.world_width = width
        self.world_height = height

        self.min_x = 1
        self.max_x = width - 2
        self.min_y = 1
        self.max_y = height - 2

        self.start = True
        self.go_home = False

        self.queue = deque() # For the new neighbours of the current position
        self.backtrack_stack = [] # For stacking a path to a certain cell in the map

    """
    Update perceived agent location
    """
    def update_position(self, bump):
        if not bump and self.last_action == ACTION_FORWARD:
            if self.direction == AGENT_DIRECTION_EAST:
                self.pos_x += 1
            elif self.direction == AGENT_DIRECTION_SOUTH:
                self.pos_y += 1
            elif self.direction == AGENT_DIRECTION_WEST:
                self.pos_x -= 1
            elif self.direction == AGENT_DIRECTION_NORTH:
                self.pos_y -= 1

    """
    Update perceived or inferred information about a part of the world
    """
    def update_world(self, x, y, info):
        self.world[x][y] = info

    """
    Dumps a map of the world as the agent knows it
    """
    def print_world_debug(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                if self.world[x][y] == AGENT_STATE_UNKNOWN:
                    print("?" if DEBUG_OPT_DENSEWORLDMAP else " ? ", end="")
                elif self.world[x][y] == AGENT_STATE_WALL:
                    print("#" if DEBUG_OPT_DENSEWORLDMAP else " # ", end="")
                elif self.world[x][y] == AGENT_STATE_CLEAR:
                    print("." if DEBUG_OPT_DENSEWORLDMAP else " . ", end="")
                elif self.world[x][y] == AGENT_STATE_DIRT:
                    print("D" if DEBUG_OPT_DENSEWORLDMAP else " D ", end="")
                elif self.world[x][y] == AGENT_STATE_HOME:
                    print("H" if DEBUG_OPT_DENSEWORLDMAP else " H ", end="")

            print() # Newline
        print() # Delimiter post-print

"""
Vacuum agent
"""
class MyVacuumAgent(Agent):

    def __init__(self, world_width, world_height, log):
        super().__init__(self.execute)
        self.initial_random_actions = 10
        self.iteration_counter = 100000
        self.state = MyAgentState(world_width, world_height)
        self.log = log

    def move_to_random_start_position(self, bump):
        action = random()

        self.initial_random_actions -= 1
        self.state.update_position(bump)

        if action < 0.1666666:   # 1/6 chance
            self.state.direction = (self.state.direction + 3) % 4
            self.state.last_action = ACTION_TURN_LEFT
            return ACTION_TURN_LEFT
        elif action < 0.3333333: # 1/6 chance
            self.state.direction = (self.state.direction + 1) % 4
            self.state.last_action = ACTION_TURN_RIGHT
            return ACTION_TURN_RIGHT
        else:                    # 4/6 chance
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD

    def execute(self, percept):

        ###########################
        # DO NOT MODIFY THIS CODE #
        ###########################

        bump = percept.attributes["bump"]
        dirt = percept.attributes["dirt"]
        home = percept.attributes["home"]

        # Move agent to a randomly chosen initial position
        if self.initial_random_actions > 0:
            self.log("Moving to random start position ({} steps left)".format(self.initial_random_actions))
            return self.move_to_random_start_position(bump)

        # Finalize randomization by properly updating position (without subsequently changing it)
        elif self.initial_random_actions == 0:
            self.initial_random_actions -= 1
            self.state.update_position(bump)
            self.state.last_action = ACTION_SUCK
            self.log("Processing percepts after position randomization")
            return ACTION_SUCK



        ########################
        # START MODIFYING HERE #
        ########################

        # Max iterations for the agent
        if self.iteration_counter < 1:
            if self.iteration_counter == 0:
                self.iteration_counter -= 1
                self.log("Iteration counter is now 0. Halting!")
                self.log("Performance: {}".format(self.performance))
            return ACTION_NOP

        self.log("Position: ({}, {})\t\tDirection: {}".format(self.state.pos_x, self.state.pos_y,
                                                              direction_to_string(self.state.direction)))

        self.iteration_counter -= 1

        # Track position of agent
        self.state.update_position(bump)

        if bump:
            # Get an xy-offset pair based on where the agent is facing
            offset = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.state.direction]

            # Mark the tile at the offset from the agent as a wall (since the agent bumped into it)
            self.state.update_world(self.state.pos_x + offset[0], self.state.pos_y + offset[1], AGENT_STATE_WALL)

        # Update perceived state of current tile
        if dirt and not home:
            self.state.update_world(self.state.pos_x, self.state.pos_y, AGENT_STATE_DIRT)
        elif not home:
            self.state.update_world(self.state.pos_x, self.state.pos_y, AGENT_STATE_CLEAR)

        # Debug
        self.state.print_world_debug()

        def turn_left():
            self.log("turning left")
            self.state.direction = (self.state.direction + 3) % 4
            self.state.last_action = ACTION_TURN_LEFT
            return ACTION_TURN_LEFT

        def turn_right():
            self.log("turning right")
            self.state.direction = (self.state.direction + 1) % 4
            self.state.last_action = ACTION_TURN_RIGHT
            return ACTION_TURN_RIGHT

        def move_forward():
            self.log("moving forward")
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD

        def go_to_start_pos():
            if self.state.direction != AGENT_DIRECTION_NORTH and self.state.pos_y > 1:
                return turn_right()
            elif home and self.state.direction != AGENT_DIRECTION_EAST:
                return turn_right()
            elif bump:
                return turn_left()
            elif (self.state.world[self.state.pos_x - 1][self.state.pos_y] == AGENT_STATE_HOME) and not(self.state.direction == AGENT_DIRECTION_EAST):
                return turn_right()
            elif (self.state.world[self.state.pos_x - 1][self.state.pos_y] == AGENT_STATE_HOME) and (self.state.direction == AGENT_DIRECTION_EAST):
                self.state.start = False
                # Do nothing
                self.state.last_action = ACTION_SUCK
                return ACTION_SUCK
            else:
                return move_forward()

        def boundary_reached():

            if self.state.min_x > self.state.max_x and self.state.min_y > self.state.max_y:
                self.log("Going Home")
                self.state.go_home = True
                return False

            if self.state.direction == AGENT_DIRECTION_EAST and self.state.pos_x == self.state.max_x:
                self.state.max_x -= 1
                return True
            elif self.state.direction == AGENT_DIRECTION_WEST and self.state.pos_x == self.state.min_x:
                self.state.min_x += 1
                return True
            elif self.state.direction == AGENT_DIRECTION_SOUTH and self.state.pos_y == self.state.max_y:
                self.state.max_y -= 1
                return True
            elif self.state.direction == AGENT_DIRECTION_NORTH and self.state.pos_y == self.state.min_y:
                self.state.min_y += 1
                return True
            return False

        def go_home():

            if self.state.direction  != AGENT_DIRECTION_NORTH and self.state.pos_y > 1:
                return turn_right()
            if home:
                self.log("Home and done!")
                self.iteration_counter = 0
                return ACTION_NOP
            elif bump:
                return turn_left()
            else:
                return move_forward()

        def update_queue():
            updated = False
            current_pos = (self.state.pos_x, self.state.pos_y)

            # Add the cell above if it's unknown/home and not already in the queue
            if self.state.world[self.state.pos_x][self.state.pos_y - 1] == AGENT_STATE_UNKNOWN or self.state.world[self.state.pos_x][self.state.pos_y - 1] == AGENT_STATE_HOME:
                new_pos = (self.state.pos_x, self.state.pos_y - 1)
                if new_pos not in [pos[0] for pos in self.state.queue]:  # Check if not in queue by comparing first elements (second is parent)
                    updated = True
                    self.state.queue.append((new_pos, current_pos))

            # Add the cell below if it's unknown/home and not already in the queue
            if self.state.world[self.state.pos_x][self.state.pos_y + 1] == AGENT_STATE_UNKNOWN or self.state.world[self.state.pos_x][self.state.pos_y + 1] == AGENT_STATE_HOME:
                new_pos = (self.state.pos_x, self.state.pos_y + 1)
                if new_pos not in [pos[0] for pos in self.state.queue]:
                    updated = True
                    self.state.queue.append((new_pos, current_pos))

            # Add the cell to the left if it's unknown/home and not already in the queue
            if self.state.world[self.state.pos_x - 1][self.state.pos_y] == AGENT_STATE_UNKNOWN or self.state.world[self.state.pos_x - 1][self.state.pos_y] == AGENT_STATE_HOME:
                new_pos = (self.state.pos_x - 1, self.state.pos_y)
                if new_pos not in [pos[0] for pos in self.state.queue]:
                    updated = True
                    self.state.queue.append((new_pos, current_pos))

            # Add the cell to the right if it's unknown/home and not already in the queue
            if self.state.world[self.state.pos_x + 1][self.state.pos_y] == AGENT_STATE_UNKNOWN or self.state.world[self.state.pos_x + 1][self.state.pos_y] == AGENT_STATE_HOME:
                new_pos = (self.state.pos_x + 1, self.state.pos_y)
                if new_pos not in [pos[0] for pos in self.state.queue]:
                    updated = True
                    self.state.queue.append((new_pos, current_pos))

            if updated:
                print("Queue updated with unknown cells: ", self.state.queue)

        def calculate_path(target):
            """
            Uses BFS to find and return path from the current position to a certain target cell
            """
            start_pos = (self.state.pos_x, self.state.pos_y)

            queue = deque()
            queue.append(start_pos)
            visited = set()
            visited.add(start_pos)
            came_from = {start_pos: None}

            while queue:
                current = queue.popleft()
                if current == target:
                    # Goal reached, reconstruct the path
                    path = []
                    while current is not None:
                        path.append(current)
                        current = came_from[current]
                    return path  # Return the path as a list

                x, y = current

                # Explore neighbors individually (left, right, up, down)

                # Left neighbor
                neighbor_x = x - 1
                neighbor_y = y
                if (self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_CLEAR or
                    self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_HOME) and (neighbor_x, neighbor_y) not in visited:
                    visited.add((neighbor_x, neighbor_y))
                    came_from[(neighbor_x, neighbor_y)] = current
                    queue.append((neighbor_x, neighbor_y))

                # Right neighbor
                neighbor_x = x + 1
                neighbor_y = y
                if (self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_CLEAR or
                    self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_HOME) and (neighbor_x, neighbor_y) not in visited:
                    visited.add((neighbor_x, neighbor_y))
                    came_from[(neighbor_x, neighbor_y)] = current
                    queue.append((neighbor_x, neighbor_y))

                # Above neighbor
                neighbor_x = x
                neighbor_y = y - 1
                if (self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_CLEAR or
                    self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_HOME) and (neighbor_x, neighbor_y) not in visited:
                    visited.add((neighbor_x, neighbor_y))
                    came_from[(neighbor_x, neighbor_y)] = current
                    queue.append((neighbor_x, neighbor_y))

                # Under neighbor
                neighbor_x = x
                neighbor_y = y + 1
                if (self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_CLEAR or
                    self.state.world[neighbor_x][neighbor_y] == AGENT_STATE_HOME) and (neighbor_x, neighbor_y) not in visited:
                    visited.add((neighbor_x, neighbor_y))
                    came_from[(neighbor_x, neighbor_y)] = current
                    queue.append((neighbor_x, neighbor_y))

            # No path found
            return None

        def directly_reachable(target_x, target_y):
            """
            Returns true if the target cell is reachable from the current cell
            """
            if target_x == self.state.pos_x and target_y == self.state.pos_y:
                return True

            # Target is directly to the left of the current position
            if target_x == self.state.pos_x - 1 and target_y == self.state.pos_y:
                return True

            # Target is directly to the right of the current position
            if target_x == self.state.pos_x + 1 and target_y == self.state.pos_y:
                return True

            # Target is directly above the current position
            if target_y == self.state.pos_y - 1 and target_x == self.state.pos_x:
                return True

            # Target is directly below the current position
            if target_y == self.state.pos_y + 1 and target_x == self.state.pos_x:
                return True

            return False

        def next_move():

            if home and self.state.go_home:
                self.log("Home and done!")
                self.iteration_counter = 0
                return ACTION_NOP

            update_queue()

            if not self.state.queue:
                self.log("The whole map is updated, lets go home")
                print("Add home to queue!")
                self.state.queue.append(((1,1), (1, 1)))
                self.state.go_home = True

            print("Queue :", self.state.queue)

            # If stack is not empty, we are on a path to a certain target
            if self.state.backtrack_stack:
                print("Stack not empty: ", self.state.backtrack_stack)
                target_x, target_y = self.state.backtrack_stack[-1]
            else:
                ((target_x, target_y), parent) = self.state.queue[0]

                if not directly_reachable(target_x, target_y) and not self.state.backtrack_stack:
                    print("Target pos not reachable: ", target_x, target_y, " looking for path...")
                    path = calculate_path(parent)
                    if path:
                        print("A path to the target: ", path)
                        self.state.backtrack_stack.extend(path)
                        target_x, target_y = self.state.backtrack_stack[-1]
                        print("new stack with path to: ",parent, self.state.backtrack_stack)

                    elif not path and (target_x, target_y) == (1, 1):
                        print("No path to home...")
                        self.iteration_counter = 0
                        return ACTION_NOP


            print("Current Position: ({}, {}) Direction: {} Target: ({}, {})".format(
                self.state.pos_x, self.state.pos_y, self.state.direction, target_x, target_y))


            if target_x == self.state.pos_x and target_y == self.state.pos_y:
                # if the target was from the stack, pop the stack to move to next target in the next call
                if self.state.backtrack_stack:
                    self.state.backtrack_stack.pop()
                    print("Backtrack stack after pop: ", self.state.backtrack_stack)
                elif self.state.queue:
                    self.state.queue.popleft()
                    print("Queue after left pop: ", self.state.queue)
                self.state.last_action = ACTION_SUCK
                return ACTION_SUCK  # Do nothing
            elif target_x < self.state.pos_x and self.state.direction != AGENT_DIRECTION_WEST:
                return turn_right()
            elif target_x > self.state.pos_x and self.state.direction != AGENT_DIRECTION_EAST:
                return turn_right()
            elif target_y < self.state.pos_y and self.state.direction != AGENT_DIRECTION_NORTH:
                return turn_right()
            elif target_y > self.state.pos_y and self.state.direction != AGENT_DIRECTION_SOUTH:
                return turn_right()
            else:
                # if the target was from the stack, pop the stack to move to next target in the next call
                if self.state.backtrack_stack:
                    self.state.backtrack_stack.pop()
                    print("Backtrack stack after pop: ", self.state.backtrack_stack)
                else:
                    self.state.queue.popleft()
                    print("Queue after left pop: ", self.state.queue)

                print("Moving forward towards: ", target_x, target_y)
                return move_forward()


        # Task2
        if dirt:
            self.state.last_action = ACTION_SUCK
            return ACTION_SUCK
        else:
            return next_move()

        # Task1
        # if dirt:
        #     self.state.last_action = ACTION_SUCK
        #     return ACTION_SUCK
        # elif self.state.start:
        #     return go_to_start_pos()
        # elif boundary_reached():
        #     return turn_right()
        # elif self.state.go_home:
        #     return go_home()
        # else:
        #     return move_forward()