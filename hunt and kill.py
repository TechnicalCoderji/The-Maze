# Import Usefull Modules
import pygame,sys
from random import choice
import json

# Set-up screen Size and grid varibles
RES = WIDTH, HEIGHT = 900,600
TILE = 60
cols, rows = WIDTH // TILE, HEIGHT // TILE
TOTAL_CELLS = cols * rows
FPS = 60

# Set-up Pygame Basic GUI code
pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Hunt And Kill Algorithm")
clock = pygame.time.Clock()

# Load System Fonts
font = pygame.font.SysFont(None, 36)

# Cell Class for Maze Cells
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    # Method for Drawing Current Cell
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color("#10f700"),(x + 2, y + 2, TILE - 2, TILE - 2),border_radius=50)

    # Method for drawing all cells in grid
    def draw(self):
        x, y = self.x * TILE, self.y * TILE

        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e1e1e'),
                             (x, y, TILE, TILE))
            
        if self.walls['top']:
            pygame.draw.line(sc, (97, 136, 199), (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, (97, 136, 199), (x + TILE, y),(x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, (97, 136, 199), (x + TILE, y + TILE),(x , y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, (97, 136, 199), (x, y + TILE), (x, y), 3)

    # Check Whether Cell Exist on Grid or Not 
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    # Return Random Neighbor of Current cell
    def check_neighbors(self):
        neighbors = []

        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
            
        return choice(neighbors) if neighbors else False
    
# remove walls Between Two Cells
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False 

# Show Percentage at Top-Center


# Initialize The Maze grid
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
grid_cells_set = set(grid_cells)
current_cell = grid_cells[0]
visted_cell = []

# Main Function For Game-loop
def main():

    # Declare global Varibles
    global grid_cells, visted_cell, current_cell

    # Game-loop
    while True:
        # Fill Screen With yellow color
        sc.fill((255,255,0))
        
        # Event Loop for handle Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        # For Draw things on screen
        [cell.draw() for cell in grid_cells]

        current_cell.visited = True
        visted_cell.append(current_cell)
        current_cell.draw_current_cell()

        

        # Hunt and Kill Algorithm Logic
        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            remove_walls(current_cell,next_cell)
            current_cell = next_cell

        else:
            for cell in grid_cells_set:
                temp_cell = cell.check_neighbors()
                if temp_cell and (cell in visted_cell):
                    current_cell = temp_cell
                    remove_walls(cell,temp_cell)
                    break
        
        # pygame GUI important code
        pygame.display.flip()
        clock.tick(FPS)

main()

# Code for save Maze data as json file
maze_array = [{'x': cell.x, 'y': cell.y, 'walls': cell.walls} for cell in grid_cells]
# print(maze_array)

file_path = 'walls_data.json'

# Save the dictionary to a file
with open(file_path, 'w') as json_file:
    json.dump(maze_array, json_file)

# for exit Pygame and command window
pygame.quit()
sys.exit()