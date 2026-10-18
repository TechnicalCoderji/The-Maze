from random import choice, sample
import heapq
from itertools import count
from maze import Grid, Pointer

# --------------- Maze Generation Algorithm ---------------

# Depth-First Search (DFS)
stack = []

def depth_first_search(maze_grid: Grid):

    global stack

    maze_grid.current_cell.visited = True

    neighbors = maze_grid.check_neighbors(maze_grid.current_cell.column, maze_grid.current_cell.row)
    next_cell = choice(neighbors) if neighbors else None
    if next_cell:
        next_cell.visited = True

        maze_grid.remove_walls(maze_grid.current_cell.column, maze_grid.current_cell.row, next_cell.column, next_cell.row)

        stack.append(maze_grid.current_cell)
        maze_grid.current_cell = next_cell
        return True

    elif stack:
        maze_grid.current_cell = stack.pop()
        return True

    else:
        return False

# Hunt and Kill Algorithm
visited_cells = set()

def hunt_and_kill(maze_grid: Grid):

    global visited_cells

    maze_grid.current_cell.visited = True
    visited_cells.add(maze_grid.current_cell)

    neighbors = maze_grid.check_neighbors(maze_grid.current_cell.column, maze_grid.current_cell.row)
    next_cell = choice(neighbors) if neighbors else None
    if next_cell:
        next_cell.visited = True

        maze_grid.remove_walls(maze_grid.current_cell.column, maze_grid.current_cell.row, next_cell.column, next_cell.row)

        maze_grid.current_cell = next_cell
        return True

    else:
        for row in sample(maze_grid.cell_grid, maze_grid.rows):
            for cell in sample(row, maze_grid.cols):
                if not cell.visited:
                    continue

                temp_neighbors = maze_grid.check_neighbors(cell.column, cell.row)
                temp_cell = choice(temp_neighbors) if temp_neighbors else None
                if temp_cell and (cell in visited_cells):
                    maze_grid.current_cell = temp_cell
                    maze_grid.remove_walls(cell.column, cell.row, temp_cell.column, temp_cell.row)
                    return True
        
        return False

# --------------- Maze Solving Algorithm ---------------

# Random Mouse Algorithm
def random_mouse(maze_grid: Grid):
    maze_grid.current_pointer.visited = True
    maze_grid.current_pointer.in_path = True

    next_pointers = maze_grid.check_neighbor_pointers(maze_grid.current_pointer.column, maze_grid.current_pointer.row)

    next_unique_pointers = []
    for pointer in next_pointers.values():
        if (not pointer.visited):
            next_unique_pointers.append(pointer)

    next_point = choice(next_unique_pointers) if next_unique_pointers else False

    if next_point:

        maze_grid.path_stack.append(maze_grid.current_pointer)

        maze_grid.make_wall(maze_grid.current_pointer.column, maze_grid.current_pointer.row, next_point.column, next_point.row)

        maze_grid.current_pointer = next_point

        return True

    elif maze_grid.path_stack:

        maze_grid.current_pointer.in_path = False
        maze_grid.current_pointer = maze_grid.path_stack.pop()

        return True

    return False

# Dead-End Fill Algorithm

# Make All Pointer Visited and in_path (Helper Function)
def explore_maze(maze_grid: Grid):

    for row in maze_grid.pointer_grid:
        for pointer in row:
            pointer.visited = True
            # pointer.in_path = True

            neighbor_pointers = maze_grid.check_neighbor_pointers(pointer.column, pointer.row)
            for neighbor_point in neighbor_pointers.values():
                maze_grid.make_wall(pointer.column, pointer.row, neighbor_point.column, neighbor_point.row)

def dead_end_fill(maze_grid: Grid):

    # Find Dead-End and Fill
    for row in maze_grid.pointer_grid:
        for pointer in row:
            # Skip if Point is Start Point or End Point
            if (pointer in (maze_grid.start_point, maze_grid.end_point)):
                continue # Not Count as Dead-End

            # Skip if Point It-self is Dead-End
            if (not pointer.visited):
                continue # Already Dead-End

            # Logic For Check Wheather it is Dead-End or Not
            # Pointer Dictinary where not wall
            neighbor_pointers =  maze_grid.check_neighbor_pointers(pointer.column, pointer.row)

            unique_neighbor_pointers = [] # Also Checked Wheather Visited or Not
            for neighbor in neighbor_pointers.values():
                if (neighbor.visited == True):
                    unique_neighbor_pointers.append(neighbor)

            # For Dead-End Condition
            if len(unique_neighbor_pointers) == 1:

                # Fill The Dead-End
                pointer.visited = False
                maze_grid.remove_pointer_wall(pointer.column, pointer.row, unique_neighbor_pointers[0].column, unique_neighbor_pointers[0].row)
                return True

    print("All Dead End Are Filled.")
    maze_grid.is_maze_Solved = True
    maze_grid.solve_algorithm = None
    maze_grid.solve_algo_is_running = False
    print("Maze Solved.")
    return False


# Right Hand (Hand Follower) Algorithm
side_tuple = ("top","right","bottom","left")

def right_hand_follower(maze_grid: Grid):
    # Initialize Direction to "left" By-Default from None
    if maze_grid.next_direction is None:
        maze_grid.next_direction = "left"

    maze_grid.current_pointer.visited = True
    maze_grid.current_pointer.in_path = True

    next_pointers = maze_grid.check_neighbor_pointers(maze_grid.current_pointer.column, maze_grid.current_pointer.row)

    # Right Hand Follower Algorithm Core
    index = side_tuple.index(maze_grid.next_direction)
    right = side_tuple[(index + 1) % 4]
    left = side_tuple[(index - 1) % 4]

    next_point = None

    # Check wall on left
    if next_pointers.get(right):
        maze_grid.next_direction = right                             # Turn right
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward

    # Check wall in front
    elif next_pointers.get(maze_grid.next_direction):
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward

    else:
        maze_grid.next_direction = left                            # Turn left
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward
    
    # Back-Track Logic
    if (next_point and (next_point not in maze_grid.path_stack)):

        maze_grid.path_stack.append(maze_grid.current_pointer)

        maze_grid.make_wall(maze_grid.current_pointer.column, maze_grid.current_pointer.row, next_point.column, next_point.row)

        maze_grid.current_pointer = next_point

        return True

    elif (maze_grid.path_stack and (next_point in maze_grid.path_stack)):

        maze_grid.current_pointer.in_path = False
        maze_grid.current_pointer = maze_grid.path_stack.pop()

        return True

    return True

# Left Hand (Hand Follower) Algorithm
def left_hand_follower(maze_grid: Grid):

    # Initialize Direction to "right" By-Default from None
    if maze_grid.next_direction is None:
        maze_grid.next_direction = "right"

    maze_grid.current_pointer.visited = True
    maze_grid.current_pointer.in_path = True

    next_pointers = maze_grid.check_neighbor_pointers(maze_grid.current_pointer.column, maze_grid.current_pointer.row)

    # Left Hand Follower Algorithm Core
    index = side_tuple.index(maze_grid.next_direction)
    right = side_tuple[(index + 1) % 4]
    left = side_tuple[(index - 1) % 4]

    next_point = None

    # Check wall on left
    if next_pointers.get(left):
        maze_grid.next_direction = left                             # Turn left
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward

    # Check wall in front
    elif next_pointers.get(maze_grid.next_direction):
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward

    else:
        maze_grid.next_direction = right                            # Turn right
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward
    
    # Back-Track Logic
    if (next_point and (next_point not in maze_grid.path_stack)):

        maze_grid.path_stack.append(maze_grid.current_pointer)

        maze_grid.make_wall(maze_grid.current_pointer.column, maze_grid.current_pointer.row, next_point.column, next_point.row)

        maze_grid.current_pointer = next_point

        return True

    elif (maze_grid.path_stack and (next_point in maze_grid.path_stack)):

        maze_grid.current_pointer.in_path = False
        maze_grid.current_pointer = maze_grid.path_stack.pop()

        return True

    return True

# A star Algorithm
actual_costs = []           # Actual cost from the start cell to the current cell
estimated_costs = []        # Estimated cost from the current cell to the goal (heuristic)
parent_cells = []           # For Path Making
open_path = []              # Priority Queue
closed_path = set()         # Empty Set
counter = count()           # Set New Counter

# Helper Funtion For A-star (Manhattan_distance - heuristic)
def manhatten_distance(start: Pointer, goal: Pointer):
    distance = abs(start.column - goal.column) + abs(start.row - goal.row)
    return distance

# For Getting Estimated Cost
def get_ecost(point: Pointer):
    cost = estimated_costs[point.row][point.column]
    return cost

# For Setting Estimated Cost
def set_ecost(point: Pointer, cost: int):
    global estimated_costs
    estimated_costs[point.row][point.column] = cost

# For Getting Actual Cost
def get_acost(point: Pointer):
    cost = actual_costs[point.row][point.column]
    return cost

# For Setting Actual Cost
def set_acost(point: Pointer, cost: int):
    global actual_costs
    actual_costs[point.row][point.column] = cost

# For Getting Parent Cell
def get_pcell(point: Pointer):
    parent = parent_cells[point.row][point.column]
    return parent

# For Setting Parent Cell
def set_pcell(point: Pointer, parent: Pointer):
    global parent_cells
    parent_cells[point.row][point.column] = parent

# Initializer Funtion For A-star
def make_score_grid(mg: Grid):

    global actual_costs, estimated_costs, parent_cells, open_path, counter

    # Reset Counter
    counter = count()

    # Set All Actual and Estimated cost to Infinity
    actual_costs = [[float("inf") for _ in range(mg.cols)] for _ in range(mg.rows)]
    estimated_costs = [[float("inf") for _ in range(mg.cols)] for _ in range(mg.rows)]

    # Set All Parents to None
    parent_cells = [[None for _ in range(mg.cols)] for _ in range(mg.rows)]

    # Initialize Values for Start cell
    set_acost(mg.start_point, 0)
    set_ecost(mg.start_point, manhatten_distance(mg.start_point, mg.end_point))

    heapq.heappush(open_path, (get_ecost(mg.start_point), next(counter), mg.start_point))

# For High-Light main Path
def ReconstructPath(mg: Grid):
    global parent_cells

    while (mg.current_pointer):
        mg.current_pointer.in_path = True
        mg.current_pointer = get_pcell(mg.current_pointer)

def a_star(mg: Grid):
    
    global actual_costs, estimated_costs, parent_cells, open_path, closed_path

    while open_path:

        # lowest Estimated Distance Selected as Current from open path queue
        mg.current_pointer = heapq.heappop(open_path)[2]

        mg.current_pointer.visited = True

        # Win Condition
        if mg.current_pointer == mg.end_point:
            ReconstructPath(mg)
            mg.is_maze_Solved = True
            mg.solve_algorithm = None
            print("Maze Solved.")
            return False

        # Add Current to closed
        closed_path.add(mg.current_pointer)

        # Get Possible Neighbors
        neighbor_pointers = mg.check_neighbor_pointers(mg.current_pointer.column, mg.current_pointer.row)

        for neighbor in neighbor_pointers.values():

            # Skip if in Closed Path
            if neighbor in closed_path:
                continue

            temp_cost = get_acost(mg.current_pointer) + 1           # Temprary Estimated Cost

            if (temp_cost < get_acost(neighbor)):

                set_pcell(neighbor, mg.current_pointer)
                set_acost(neighbor, temp_cost)
                set_ecost(neighbor, (get_acost(neighbor) + manhatten_distance(neighbor, mg.end_point)))

                mg.make_wall(mg.current_pointer.column, mg.current_pointer.row, neighbor.column, neighbor.row)

                heapq.heappush(open_path, (get_ecost(neighbor), next(counter), neighbor))

        return True

    return False

# Dijkstra Algorithm
def dijkstra(maze_grid: Grid):
    pass