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
        for row in maze_grid.grid:
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
