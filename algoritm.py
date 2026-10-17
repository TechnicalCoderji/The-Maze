from random import choice
from maze import Grid

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
        for row in maze_grid.cell_grid:
            for cell in row:
                if not cell.visited:
                    continue

                temp_neighbors = maze_grid.check_neighbors(cell.column, cell.row)
                temp_cell = choice(temp_neighbors) if temp_neighbors else None
                if temp_cell and (cell in visited_cells):
                    maze_grid.current_cell = temp_cell
                    maze_grid.remove_walls(cell.column, cell.row, temp_cell.column, temp_cell.row)
                    return True
        
        return False

# --------------- Maze Generation Algorithm ---------------

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
def dead_end_fill(maze_grid: Grid):
    pass

# Right Hand (Hand Follower) Algorithm
def right_hand_follower(maze_grid: Grid):
    pass

# Left Hand (Hand Follower) Algorithm
def left_hand_follower(maze_grid: Grid):
    pass

# A star Algorithm
def a_star(maze_grid: Grid):
    pass

# Dijkstra Algorithm
def dijkstra(maze_grid: Grid):
    pass