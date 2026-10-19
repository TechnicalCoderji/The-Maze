# Brain of the project: This Module Contains Algorithm and helper funtions for Algorithms

# External Imports for algorithm
from random import choice, sample
import heapq
from itertools import count

# Internal Imports For Reference Suggestion
from maze import Grid, Pointer

# --------------- Maze Generation Algorithm ---------------

# Depth-First Search (DFS) - solve maze by backtracking when stuck
stack = []      # Used for Backtrack

# Main Algorithm Funtion to Give step-by-step Animation for Depth-First Search Maze Generation Algorithm
def depth_first_search(maze_grid: Grid):

    global stack

    maze_grid.current_cell.visited = True

    # Get valid neighbors of current cell
    neighbors = maze_grid.check_neighbors(maze_grid.current_cell.column, maze_grid.current_cell.row)
    next_cell = choice(neighbors) if neighbors else None

    # Move to new next cell
    if next_cell:
        next_cell.visited = True

        # Remove walls between current cell and next cell
        maze_grid.remove_walls(maze_grid.current_cell.column, maze_grid.current_cell.row, next_cell.column, next_cell.row)

        # Append to Stack for Future Backtraking
        stack.append(maze_grid.current_cell)
        maze_grid.current_cell = next_cell
        return True

    # Backtrack cell from existing stack
    elif stack:
        maze_grid.current_cell = stack.pop()
        return True

    else:
        # Algorithm Finished Maze Generated Successfully
        return False

# Hunt and Kill Algorithm - solve maze by hunt(selecting) random next cell from grid when stuck
visited_cells = set()       # For store visited cell to Hunt new cell efficiently

# Main Algorithm Funtion to Give step-by-step Animation for Hunt & Kill Maze Generation Algorithm
def hunt_and_kill(maze_grid: Grid):

    global visited_cells

    maze_grid.current_cell.visited = True
    visited_cells.add(maze_grid.current_cell)

    # Get valid neighbors of current cell
    neighbors = maze_grid.check_neighbors(maze_grid.current_cell.column, maze_grid.current_cell.row)
    next_cell = choice(neighbors) if neighbors else None

    # Move to new next cell
    if next_cell:
        next_cell.visited = True

        # Remove walls between current cell and next cell
        maze_grid.remove_walls(maze_grid.current_cell.column, maze_grid.current_cell.row, next_cell.column, next_cell.row)

        maze_grid.current_cell = next_cell
        return True

    # For Hunt New Cell Randomly
    else:

        # Scan Whole Grid
        for row in sample(maze_grid.cell_grid, maze_grid.rows):
            for cell in sample(row, maze_grid.cols):

                # Skip cell that is already visited
                if not cell.visited:
                    continue

                # get and check neighbors of each cell to verify whether that is in visited cells or not
                temp_neighbors = maze_grid.check_neighbors(cell.column, cell.row)
                temp_cell = choice(temp_neighbors) if temp_neighbors else None

                # Logic to hunt new founded cell
                if temp_cell and (cell in visited_cells):
                    maze_grid.current_cell = temp_cell

                    # Remove walls between Hunted cell and neighbor(temp/in_path) cell
                    maze_grid.remove_walls(cell.column, cell.row, temp_cell.column, temp_cell.row)

                    return True

        # Algorithm Finished Maze Generated Successfully
        return False

# --------------- Maze Solving Algorithm ---------------

# Random Mouse Algorithm - Solve maze by choosing random next direction
def random_mouse(maze_grid: Grid):

    # Make current poninter visited and in_path
    maze_grid.current_pointer.visited = True
    maze_grid.current_pointer.in_path = True

    # Get Valid Next Pointer dict with direction as key and pointer as value
    next_pointers = maze_grid.check_neighbor_pointers(maze_grid.current_pointer.column, maze_grid.current_pointer.row)

    # For filtering already visited pointers
    next_unique_pointers = []
    for pointer in next_pointers.values():
        if (not pointer.visited):
            next_unique_pointers.append(pointer)

    # Randomly select one neighbor from filtered list
    next_point = choice(next_unique_pointers) if next_unique_pointers else False

    if next_point:

        # Use path_stack for future backtracking
        maze_grid.path_stack.append(maze_grid.current_pointer)

        # Create Connection(wall) between current pointer and next pointer
        maze_grid.make_wall(maze_grid.current_pointer.column, maze_grid.current_pointer.row, next_point.column, next_point.row)

        # Move current pointer to next pointer
        maze_grid.current_pointer = next_point

        return True

    # For bakctrack if getting stuck in Dead-End
    elif maze_grid.path_stack:

        # Set that pointer not in path and then pop stack to get previews pointer
        maze_grid.current_pointer.in_path = False
        maze_grid.current_pointer = maze_grid.path_stack.pop()

        return True

    # Algorithm Finished, Maze Solved
    return False

# Dead-End Fill Algorithm - Solve maze by filling Dead-End one-by-one

# Make All Pointer Visited and in_path (Helper Function)
def explore_maze(maze_grid: Grid):

    # Loop throw full pointer grid
    for row in maze_grid.pointer_grid:
        for pointer in row:
            pointer.visited = True
            # pointer.in_path = True

            # Get valid neighbor pointers
            neighbor_pointers = maze_grid.check_neighbor_pointers(pointer.column, pointer.row)

            # Create connection from pointer to all neighbor
            for neighbor_point in neighbor_pointers.values():
                maze_grid.make_wall(pointer.column, pointer.row, neighbor_point.column, neighbor_point.row)

# Main Algorithm Funtion to Give step-by-step Animation for Dead-End Fill Maze Solving Algorithm
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
            # Valid neighbor pointer dictinary
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

    # Algorithm Finished, Maze Solved
    print("All Dead End Are Filled.")

    # Set all values to default
    maze_grid.is_maze_Solved = True
    maze_grid.solve_algorithm = None
    maze_grid.solve_algo_is_running = False
    print("Maze Solved.")
    return False


# Right Hand (Hand Follower) Algorithm - Follow all path at right side and follow right side wall 

# Used to get next direction after roatating left(anticlockwise) and right(clockwise)
side_tuple = ("top","right","bottom","left")

# Main Algorithm Funtion to Give step-by-step Animation for Right-Hand Maze Solver Algorithm
def right_hand_follower(maze_grid: Grid):

    # Initialize Direction to "left" By-Default from None
    if maze_grid.next_direction is None:
        maze_grid.next_direction = "left"

    # Make current poninter visited and in_path
    maze_grid.current_pointer.visited = True
    maze_grid.current_pointer.in_path = True

    # Get valid neighbor pointer dict
    next_pointers = maze_grid.check_neighbor_pointers(maze_grid.current_pointer.column, maze_grid.current_pointer.row)

    # Right Hand Follower Algorithm Core
    index = side_tuple.index(maze_grid.next_direction)
    right = side_tuple[(index + 1) % 4]
    left = side_tuple[(index - 1) % 4]

    next_point = None

    # Check wall on left
    if next_pointers.get(right):
        maze_grid.next_direction = right                            # Turn right
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward

    # Check wall in front
    elif next_pointers.get(maze_grid.next_direction):
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward

    else:
        maze_grid.next_direction = left                             # Turn left
        next_point = next_pointers.get(maze_grid.next_direction)    # Move forward
    
    # Follow main right path
    if (next_point and (next_point not in maze_grid.path_stack)):

        maze_grid.path_stack.append(maze_grid.current_pointer)

        # Create Connection(wall) between current pointer and next pointer
        maze_grid.make_wall(maze_grid.current_pointer.column, maze_grid.current_pointer.row, next_point.column, next_point.row)

        maze_grid.current_pointer = next_point

        return True

    # Back-track when stuck in dead-end
    elif (maze_grid.path_stack and (next_point in maze_grid.path_stack)):

        maze_grid.current_pointer.in_path = False
        maze_grid.current_pointer = maze_grid.path_stack.pop()

        return True

    return True

# Left Hand (Hand Follower) Algorithm
# Main Algorithm Funtion to Give step-by-step Animation for Left-Hand Maze Solver Algorithm
def left_hand_follower(maze_grid: Grid):

    # Initialize Direction to "right" By-Default from None
    if maze_grid.next_direction is None:
        maze_grid.next_direction = "right"

    # Make current poninter visited and in_path
    maze_grid.current_pointer.visited = True
    maze_grid.current_pointer.in_path = True

    # Get valid neighbor pointer dict
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
    
    # Follow main left path
    if (next_point and (next_point not in maze_grid.path_stack)):

        maze_grid.path_stack.append(maze_grid.current_pointer)

        # Create Connection(wall) between current pointer and next pointer
        maze_grid.make_wall(maze_grid.current_pointer.column, maze_grid.current_pointer.row, next_point.column, next_point.row)

        maze_grid.current_pointer = next_point

        return True

    # Back-track when stuck in dead-end
    elif (maze_grid.path_stack and (next_point in maze_grid.path_stack)):

        maze_grid.current_pointer.in_path = False
        maze_grid.current_pointer = maze_grid.path_stack.pop()

        return True

    return True

# A star Algorithm

# Varible needed for A* and Dijkstra's Algorithm
actual_costs = []           # Actual cost from the start cell to the current cell
estimated_costs = []        # Estimated cost from the current cell to the goal (heuristic)
parent_cells = []           # For Reverse Path Making
open_path = []              # Priority Queue (min-heap)
closed_path = set()         # Empty Set
counter = count()           # Set New Counter

# Helper Funtion For A-star (Manhattan_distance - heuristic)
def manhatten_distance(start: Pointer, goal: Pointer):
    distance = abs(start.column - goal.column) + abs(start.row - goal.row)
    return distance

# Get or Set data in 2D list from Pointer data-type

# Estimated Cost
# For Getting Estimated Cost
def get_ecost(point: Pointer):
    cost = estimated_costs[point.row][point.column]
    return cost

# For Setting Estimated Cost
def set_ecost(point: Pointer, cost: int):
    global estimated_costs
    estimated_costs[point.row][point.column] = cost

# Actual Cost
# For Getting Actual Cost
def get_acost(point: Pointer):
    cost = actual_costs[point.row][point.column]
    return cost

# For Setting Actual Cost
def set_acost(point: Pointer, cost: int):
    global actual_costs
    actual_costs[point.row][point.column] = cost

# Patent Cell
# For Getting Parent Cell
def get_pcell(point: Pointer):
    parent = parent_cells[point.row][point.column]
    return parent

# For Setting Parent Cell
def set_pcell(point: Pointer, parent: Pointer):
    global parent_cells
    parent_cells[point.row][point.column] = parent

# Initializer Funtion For A-star
def initialize_a_star(mg: Grid):

    global actual_costs, estimated_costs, parent_cells, open_path, counter

    # Reset Counter and Open Path
    counter = count()
    open_path = []

    # Set All Actual and Estimated cost to Infinity
    actual_costs = [[float("inf") for _ in range(mg.cols)] for _ in range(mg.rows)]
    estimated_costs = [[float("inf") for _ in range(mg.cols)] for _ in range(mg.rows)]

    # Set All Parents to None
    parent_cells = [[None for _ in range(mg.cols)] for _ in range(mg.rows)]

    # Initialize Values for Start cell
    set_acost(mg.start_point, 0)
    set_ecost(mg.start_point, manhatten_distance(mg.start_point, mg.end_point))

    # Add first(current) cell to open_path
    heapq.heappush(open_path, (get_ecost(mg.start_point), next(counter), mg.start_point))

# For Reverse Path Making
def ReconstructPath(mg: Grid):
    global parent_cells

    # Back path making one-by-one from parent_cell array
    while (mg.current_pointer):
        mg.current_pointer.in_path = True
        mg.current_pointer = get_pcell(mg.current_pointer)
        return True

    # Reverse Path generated successfully
    mg.is_maze_Solved = True
    mg.solve_algorithm = None
    print("Maze Path Solved.")
    return False

# Main Algorithm Funtion to Give step-by-step Animation for A-Star Maze Solver Algorithm
def a_star(mg: Grid):
    
    global actual_costs, estimated_costs, parent_cells, open_path, closed_path

    # Loop throw priority queue
    while open_path:

        # lowest Estimated Distance Selected as Current from open path queue
        mg.current_pointer = heapq.heappop(open_path)[2]

        # Mark current as visited
        mg.current_pointer.visited = True

        # Win Condition
        if mg.current_pointer == mg.end_point:
            # Algorithm Finished, Maze Solved
            print("Maze Solved.")
            mg.solve_algorithm = ReconstructPath

            # For reverse path making
            ReconstructPath(mg)
            return True

        # Add Current to closed
        closed_path.add(mg.current_pointer)

        # Get Possible Valid Neighbors
        neighbor_pointers = mg.check_neighbor_pointers(mg.current_pointer.column, mg.current_pointer.row)

        # Loop throw each neighbor
        for neighbor in neighbor_pointers.values():

            # Skip if in Closed Path
            if neighbor in closed_path:
                continue

            # Temprary Estimated Cost
            temp_cost = get_acost(mg.current_pointer) + 1

            # Condition for cost checking
            if (temp_cost < get_acost(neighbor)):

                # Update all cost to new values
                set_pcell(neighbor, mg.current_pointer)
                set_acost(neighbor, temp_cost)
                set_ecost(neighbor, (get_acost(neighbor) + manhatten_distance(neighbor, mg.end_point)))

                # Create Connection(wall) between current pointer and neighbor pointer
                mg.make_wall(mg.current_pointer.column, mg.current_pointer.row, neighbor.column, neighbor.row)

                # Add neighbor to priority queue for process in next itration
                heapq.heappush(open_path, (get_ecost(neighbor), next(counter), neighbor))

        return True

    # Algorithm Finished
    return False

# Dijkstra Algorithm

# Initializer Funtion For Dijkstra Algorithm
def initialize_dijkstra(mg: Grid):

    global open_path, actual_costs, parent_cells, counter

    # Reset Open Path and Counter
    counter = count()
    open_path = []

    # Set All Actual cost to Infinity
    actual_costs = [[float("inf") for _ in range(mg.cols)] for _ in range(mg.rows)]

    # Set All Parents to None
    parent_cells = [[None for _ in range(mg.cols)] for _ in range(mg.rows)]

    # Set Distance of Start (We use Distance as Actual Costs)
    set_acost(mg.start_point, 0)

    # Push First Point to Priority Queue
    heapq.heappush(open_path, (get_acost(mg.start_point), next(counter), mg.start_point))


def dijkstra_algorithm(mg: Grid):

    global open_path, actual_costs, parent_cells, counter

    # Loop throw priority queue
    while open_path:

        # Remove Element with Smallest distance from open_path
        mg.current_pointer = heapq.heappop(open_path)[2]

        # Skip Pointer which is Already Visited
        if mg.current_pointer.visited:
            continue

        # Mark current as visited
        mg.current_pointer.visited = True

        # Win Condition
        if mg.current_pointer == mg.end_point:
            # Algorithm Finished, Maze Solved
            print("Maze Solved.")
            mg.solve_algorithm = ReconstructPath

            # For reverse path making
            ReconstructPath(mg) # Same of A* and Dijkstra's Algorithm
            return True

        # Get Possible Neighbors
        neighbor_pointers = mg.check_neighbor_pointers(mg.current_pointer.column, mg.current_pointer.row)

        # Loop throw each neighbor
        for neighbor in neighbor_pointers.values():

            # Skip Neighbor which is Already visited
            if neighbor.visited:
                continue

            # New Cell/Pointer Distance from Start
            new_distance = get_acost(mg.current_pointer) + 1

            # Condition for cost checking
            if (new_distance < get_acost(neighbor)):

                # Update all cost to new values
                set_acost(neighbor, new_distance)
                set_pcell(neighbor, mg.current_pointer)

                # Create Connection(wall) between current pointer and neighbor pointer
                mg.make_wall(mg.current_pointer.column, mg.current_pointer.row, neighbor.column, neighbor.row)

                # Add neighbor to priority queue for process in next itration
                heapq.heappush(open_path, (new_distance, next(counter), neighbor))

        return True

    # Algorithm Finished
    return False