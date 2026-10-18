# This File For Save and Load Maze From/To ".json" File.
import json
from maze import Cell

# For Save Sudoku from Board to as a File
def save_sudoku(file_name, maze_grid):

    # making JSON file from maze_grid
    grid = [[0 for _ in range(maze_grid.cols)] for _ in range(maze_grid.rows)]

    WALL_TOP = 1
    WALL_RIGHT = 2
    WALL_BOTTOM = 4
    WALL_LEFT = 8

    for rows in maze_grid.cell_grid:
        for cell in rows:
            bitmask = 0

            walls = cell.walls

            if walls['top']:
                bitmask |= WALL_TOP     # Top wall
            if walls['right']:
                bitmask |= WALL_RIGHT   # Right wall
            if walls['bottom']:
                bitmask |= WALL_BOTTOM  # Bottom wall
            if walls['left']:
                bitmask |= WALL_LEFT    # Left wall

            grid[cell.row][cell.column] = bitmask

    maze_dict = {
        "rows": maze_grid.rows,
        "cols": maze_grid.cols,
        "grid": grid
    }

    # Save Json to file
    final_file_name = "MazeGrids/"+file_name+".json"
    with open(final_file_name, "w") as file:
        json.dump(maze_dict, file)

# For Load Sudoku from File to as a Board
def load_sudoku(file_name, maze_grid):
    # Check for row and column compatability later

    final_file_name = "MazeGrids/"+file_name+".json"

    with open(final_file_name,"r") as file:
        maze_data = json.load(file)

    rows = maze_data["rows"]
    cols = maze_data["cols"]

    # Add Validation For Row and Column Compatable with Maze Grid
    if not (rows == maze_grid.rows and cols == maze_grid.cols):
        print("Error: Grid Size Not Compatable.")
        return False

    grid_bitmask = maze_data["grid"]

    WALL_TOP = 1
    WALL_RIGHT = 2
    WALL_BOTTOM = 4
    WALL_LEFT = 8

    for y in range(rows):
        for x in range(cols):
            bitmask = grid_bitmask[y][x]
            walls = {
                'top': bool(bitmask & WALL_TOP),
                'right': bool(bitmask & WALL_RIGHT),
                'bottom': bool(bitmask & WALL_BOTTOM),
                'left': bool(bitmask & WALL_LEFT)
            }

            maze_grid.cell_grid[y][x].walls = walls
            maze_grid.cell_grid[y][x].visited = True  # Mark the cell as visited after loading

    return True

if __name__=="__main__":
    pass