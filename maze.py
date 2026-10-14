import pygame

class Cell:
    def __init__(self, start_x, start_y, column, row, tile_size, line_color, line_width):
        self.start_x = start_x
        self.start_y = start_y
        self.column = column
        self.row = row
        self.tile = tile_size
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.line_color = line_color
        self.line_width = line_width

    def draw(self, sc: pygame.Surface):
        x, y = self.start_x + self.column * self.tile, self.start_y + self.row * self.tile
        
        if self.walls['top']:
            pygame.draw.line(sc, self.line_color, (x, y), (x + self.tile, y), self.line_width)
            
        if self.walls['right']:
            pygame.draw.line(sc, self.line_color, (x + self.tile, y), (x + self.tile, y + self.tile), self.line_width)
            
        if self.walls['bottom']:
            pygame.draw.line(sc, self.line_color, (x + self.tile, y + self.tile),(x , y + self.tile), self.line_width)
            
        if self.walls['left']:
            pygame.draw.line(sc, self.line_color, (x, y + self.tile), (x, y), self.line_width)

class Grid:
    def __init__(self, start_x, start_y, width, height, tile_size, line_color):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cols = width // tile_size
        self.rows = height // tile_size
        self.tile = tile_size
        self.grid_line_color = line_color
        self.grid_line_width = (tile_size*10)//100
        self.grid = [[Cell(self.start_x, self.start_y, col, row, tile_size, self.grid_line_color, self.grid_line_width) for col in range(self.cols)] for row in range(self.rows)]
        self.TOTAL_CELLS = self.cols * self.rows
        self.MAZE_Box_Border_Width = 7

        # colors
        self.MAZE_Box_Color = (0, 0, 0)

    def draw(self, sc: pygame.Surface):
        # Main Maze Grid Rectangle
        pygame.draw.rect(sc, self.MAZE_Box_Color, (self.start_x, self.start_y, self.width, self.height), 0)
        pygame.draw.rect(sc, self.grid_line_color, (self.start_x - self.MAZE_Box_Border_Width, self.start_y - self.MAZE_Box_Border_Width, self.width + 2 * self.MAZE_Box_Border_Width, self.height + 2 * self.MAZE_Box_Border_Width), self.MAZE_Box_Border_Width, 10)

        # Maze Grid Cells
        for row in self.grid:
            for cell in row:
                cell.draw(sc)