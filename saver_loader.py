# This Module For Save and Load Maze From/To ".json" File.
import json

# For Save maze from Grid to as .json File
def save_maze(file_name, maze_grid):

    # making JSON file from maze_grid

    # Set 2D grid with 0
    grid = [[0 for _ in range(maze_grid.cols)] for _ in range(maze_grid.rows)]

    # Assign bit Value to wall direction for Bitmask
    WALL_TOP = 1
    WALL_RIGHT = 2
    WALL_BOTTOM = 4
    WALL_LEFT = 8

    # Loop throw maze to make bitmask grid for saving
    for rows in maze_grid.cell_grid:
        for cell in rows:

            # Bit-mask Encoding Logic
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

    # Make dictionary data to dump as json in file
    maze_dict = {
        "rows": maze_grid.rows,
        "cols": maze_grid.cols,
        "grid": grid
    }

    # Save dictinary to json file
    final_file_name = "MazeGrids/" + file_name + ".json"
    with open(final_file_name, "w") as file:
        json.dump(maze_dict, file)

# For Load Maze from .json File to as a Grid
def load_maze(file_name, maze_grid):
    
    # Create file name for load
    final_file_name = "MazeGrids/" + file_name + ".json"

    # load data from json file to pthon dictinary
    with open(final_file_name,"r") as file:
        maze_data = json.load(file)

    # Get Rows and Cols form dictinary
    rows = maze_data["rows"]
    cols = maze_data["cols"]

    # Add Validation For Row and Column Compatable with Maze Grid
    if not (rows == maze_grid.rows and cols == maze_grid.cols):
        print("Error: Grid Size Not Compatable.")
        return False

    # Load bitmask data from dictinary
    grid_bitmask = maze_data["grid"]

    # Assign bit Value to wall direction for Bitmask
    WALL_TOP = 1
    WALL_RIGHT = 2
    WALL_BOTTOM = 4
    WALL_LEFT = 8

    # Loop throw rows and cols(whole grid) to assign bimask to object attributes
    for y in range(rows):
        for x in range(cols):

            # Bitmask Decoding Logic
            bitmask = grid_bitmask[y][x]
            walls = {
                'top': bool(bitmask & WALL_TOP),
                'right': bool(bitmask & WALL_RIGHT),
                'bottom': bool(bitmask & WALL_BOTTOM),
                'left': bool(bitmask & WALL_LEFT)
            }

            # Set cell data
            maze_grid.cell_grid[y][x].walls = walls
            maze_grid.cell_grid[y][x].visited = True

    return True

if __name__=="__main__":
    pass