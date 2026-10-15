import pygame

class Cell:
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, sc: pygame.Surface, x, y, tile_size, line_color, line_width):

        if not self.visited:
            pygame.draw.rect(sc, (37, 76, 139), (x, y, tile_size, tile_size))
        
        if self.walls['top']:
            pygame.draw.line(sc, line_color, (x, y), (x + tile_size, y), line_width)
            
        if self.walls['right']:
            pygame.draw.line(sc, line_color, (x + tile_size, y), (x + tile_size, y + tile_size), line_width)
            
        if self.walls['bottom']:
            pygame.draw.line(sc, line_color, (x + tile_size, y + tile_size),(x , y + tile_size), line_width)
            
        if self.walls['left']:
            pygame.draw.line(sc, line_color, (x, y + tile_size), (x, y), line_width)

    def draw_current_cell(self, sc: pygame.Surface, x, y, tile_size, padding):

        pygame.draw.rect(sc, pygame.Color('#f70067'),(x + padding, y + padding, tile_size - (2*padding), tile_size - (2*padding)),border_radius=20)

class Grid:
    def __init__(self, start_x, start_y, width, height, tile_size, line_color):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.tile = tile_size
        self.grid_line_color = line_color

        self.grid_line_width = (tile_size*10)//100
        self.cols = width // tile_size
        self.rows = height // tile_size
        self.TOTAL_CELLS = self.cols * self.rows
        self.padding = (tile_size*10)//100

        self.grid = [[Cell(col, row) for col in range(self.cols)] for row in range(self.rows)]

        # Generation Algorithm Attributes
        self.current_cell = self.grid[0][0]
        self.algorithm = None
        self.algo_is_running = False

        # Fix Varibles
        self.MAZE_Box_Border_Width = 7
        self.MAZE_Box_Color = (0, 0, 0)

    def draw(self, sc: pygame.Surface):
        # Main Maze Grid Rectangle
        pygame.draw.rect(sc, self.MAZE_Box_Color, (self.start_x, self.start_y, self.width, self.height), 0)
        pygame.draw.rect(sc, self.grid_line_color, (self.start_x - self.MAZE_Box_Border_Width, self.start_y - self.MAZE_Box_Border_Width, self.width + 2 * self.MAZE_Box_Border_Width, self.height + 2 * self.MAZE_Box_Border_Width), self.MAZE_Box_Border_Width, 10)

        # Maze Grid Cells
        for row in self.grid:
            for cell in row:
                x, y = self.start_x + cell.column * self.tile, self.start_y + cell.row * self.tile
                cell.draw(sc, x, y, self.tile, self.grid_line_color, self.grid_line_width)

        # For Current Cell Drawing
        if self.algo_is_running:
            x, y = self.start_x + self.current_cell.column * self.tile, self.start_y + self.current_cell.row * self.tile
            self.current_cell.draw_current_cell(sc, x, y, self.tile, self.padding)
            self.algo_is_running = self.algorithm(self)

            if not self.algo_is_running:
                self.algorithm = None

    def check_cell(self, x, y):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        return self.grid[y][x]

    def check_neighbors(self, x, y):
        neighbors = []

        top = self.check_cell(x, y - 1)
        right = self.check_cell(x + 1, y)
        bottom = self.check_cell(x, y + 1)
        left = self.check_cell(x - 1, y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return neighbors

    # remove walls betweem two cells
    def remove_walls(self,current_x, current_y, next_x, next_y):

        dx = current_x - next_x

        if dx == 1:
            self.grid[current_y][current_x].walls['left'] = False
            self.grid[next_y][next_x].walls['right'] = False
        elif dx == -1:
            self.grid[current_y][current_x].walls['right'] = False
            self.grid[next_y][next_x].walls['left'] = False

        dy = current_y - next_y
        if dy == 1:
            self.grid[current_y][current_x].walls['top'] = False
            self.grid[next_y][next_x].walls['bottom'] = False
        elif dy == -1:
            self.grid[current_y][current_x].walls['bottom'] = False
            self.grid[next_y][next_x].walls['top'] = False