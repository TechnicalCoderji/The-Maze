# This module is for Seperate maze related pygame and algorithm implementation logic from main code

import pygame

# Represent Individual cell
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

# Represent Our Position on Maze(Poining to cell)
class Pointer:

    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.connects = {'top': False, 'right': False, 'bottom': False, 'left': False}
        self.visited = False
        self.in_path = False

    def draw(self, sc: pygame.Surface, x, y, radius, line_color, rect_width):

        pygame.draw.circle(sc, line_color, (x,y), radius)
        
        if self.connects['top']:
            pygame.draw.rect(sc, line_color, (x-radius, y-rect_width, radius*2,  rect_width+1))
        if self.connects['right']:
            pygame.draw.rect(sc, line_color, (x, y-radius, rect_width+1, radius*2))
        if self.connects['bottom']:
            pygame.draw.rect(sc, line_color, (x-radius, y, radius*2, rect_width+1))
        if self.connects['left']:
            pygame.draw.rect(sc, line_color, (x-rect_width, y-radius, rect_width+1,radius*2))

    def draw_current_pointer(self, sc: pygame.Surface, x, y, radius):

        pygame.draw.circle(sc, (0,0,200), (x,y), radius)

    def draw_special_pointer(self, sc: pygame.Surface, x, y, radius, color):

        pygame.draw.circle(sc, color, (x,y), radius)

# Combine Cell and Pointer for maze pygame UI drawing and algorithm logic
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
        self.radius = self.tile//5
        self.rect_width = self.tile//2

        self.cell_grid = [[Cell(col, row) for col in range(self.cols)] for row in range(self.rows)]
        self.pointer_grid = [[Pointer(col, row) for col in range(self.cols)] for row in range(self.rows)]

        # Solving Algorithm By-Default Variables
        self.current_pointer = self.pointer_grid[0][0]
        self.path_stack = []
        self.next_direction = None
        self.start_point = self.pointer_grid[0][0]
        self.end_point = self.pointer_grid[self.rows-1][self.cols-1]

        # Solving Algorithm Attributes
        self.solve_algorithm = None
        self.solve_algo_is_running = False
        self.is_maze_Solved = False

        # Generation Algorithm Attributes
        self.current_cell = self.cell_grid[0][0]
        self.gen_algorithm = None
        self.gen_algo_is_running = False
        self.is_maze_Generated = False

        # Fix Varibles
        self.MAZE_Box_Border_Width = 7
        self.MAZE_Box_Color = (0, 0, 0)

    def reset_solve(self):
        self.pointer_grid = [[Pointer(col, row) for col in range(self.cols)] for row in range(self.rows)]

        self.current_pointer = self.pointer_grid[0][0]
        self.path_stack = []
        self.next_direction = None
        self.start_point = self.pointer_grid[0][0]
        self.end_point = self.pointer_grid[self.rows-1][self.cols-1]

        self.solve_algorithm = None
        self.solve_algo_is_running = False
        self.is_maze_Solved = False

    def handle_events(self, event: pygame.event.Event):

        if ((self.is_maze_Generated) and (self.solve_algorithm is None) and (not self.is_maze_Solved)):

            # KeyBoard Key to Move Maze Pointer (Manual Solve)
            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_w, pygame.K_UP):
                    self.next_direction = "top"

                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    self.next_direction = "left"

                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    self.next_direction = "bottom"

                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.next_direction = "right"

    def draw(self, sc: pygame.Surface):
        # Main Maze Grid Rectangle
        pygame.draw.rect(sc, self.MAZE_Box_Color, (self.start_x, self.start_y, self.width, self.height), 0)
        pygame.draw.rect(sc, self.grid_line_color, (self.start_x - self.MAZE_Box_Border_Width, self.start_y - self.MAZE_Box_Border_Width, self.width + 2 * self.MAZE_Box_Border_Width, self.height + 2 * self.MAZE_Box_Border_Width), self.MAZE_Box_Border_Width, 10)

        # Maze Grid Cells
        for row in self.cell_grid:
            for cell in row:
                x, y = self.start_x + cell.column * self.tile, self.start_y + cell.row * self.tile
                cell.draw(sc, x, y, self.tile, self.grid_line_color, self.grid_line_width)

        # For Current Cell Drawing and Algorithm Function Call
        if self.gen_algo_is_running:
            x, y = self.start_x + self.current_cell.column * self.tile, self.start_y + self.current_cell.row * self.tile
            self.current_cell.draw_current_cell(sc, x, y, self.tile, self.padding)
            self.gen_algo_is_running = self.gen_algorithm(self)

            if not self.gen_algo_is_running:
                self.gen_algorithm = None
                self.is_maze_Generated = True

        # For Generation Completed (Manual Solve & Algorithms)
        elif self.is_maze_Generated:

            # For Path Drawing out of Pointers which are visited
            for row in self.pointer_grid:
                for pointer in row:
                    x = self.start_x + (pointer.column * self.tile)+(self.rect_width)
                    y = self.start_y + (pointer.row * self.tile)+(self.rect_width)

                    # For Start Point
                    if (pointer == self.start_point):
                        pointer.draw_special_pointer(sc, x, y, (self.tile//3), (200, 0, 0))

                    # For End Point
                    elif (pointer == self.end_point):
                        pointer.draw_special_pointer(sc, x, y, (self.tile//3), (0, 200, 0))

                    if pointer.visited:
                        
                        line_color = (3, 211, 252) if pointer.in_path else (255, 255, 255)
                        pointer.draw(sc, x, y, self.radius, line_color, self.rect_width)

                        # For Current Pointer Drawing
                        if pointer == self.current_pointer:
                            self.current_pointer.draw_current_pointer(sc, x, y, self.radius)

            # For Maze State Update Logic (Manual)
            if ((self.solve_algorithm is None) and (not self.is_maze_Solved)):
                # Win Condition Check
                if (self.current_pointer == self.end_point):
                    self.is_maze_Solved = True
                    self.solve_algorithm = None
                    self.solve_algo_is_running = False
                    print("Maze Solved.")

                self.manual_solve_algorithm()

            # For Maze State Update Logic (Algorithm)
            elif self.solve_algo_is_running:

                # Win Condition Check
                if (self.current_pointer == self.end_point):
                    # Make Last Cell visited True
                    self.end_point.visited = True
                    self.end_point.in_path = True

                    self.is_maze_Solved = True
                    self.solve_algorithm = None
                    self.solve_algo_is_running = False
                    print("Maze Solved.")

                else:
                    self.solve_algo_is_running = self.solve_algorithm(self)

    def manual_solve_algorithm(self):

        self.current_pointer.visited = True
        self.current_pointer.in_path = True

        next_pointers = self.check_neighbor_pointers(self.current_pointer.column, self.current_pointer.row)

        if self.next_direction:
            next_point = next_pointers.get(self.next_direction)
            if next_point and (next_point not in self.path_stack):

                self.path_stack.append(self.current_pointer)

                self.make_wall(self.current_pointer.column, self.current_pointer.row, next_point.column, next_point.row)

                self.current_pointer = next_point

            elif self.path_stack and (next_point in self.path_stack):

                self.current_pointer.in_path = False
                self.current_pointer = self.path_stack.pop()

            self.next_direction = None

    # Check Cell Exist in Grid or Not (Generation Algorithm)
    def check_cell(self, x, y):
        if (x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1):
            return False
        
        return self.cell_grid[y][x]

    # Give All Possible Not Visited Neighbor Cells (Generation Algorithm)
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

    # Remove Walls Betweem Two Cells (Generation Algorithm)
    def remove_walls(self,current_x, current_y, next_x, next_y):

        dx = current_x - next_x

        if dx == 1:
            self.cell_grid[current_y][current_x].walls['left'] = False
            self.cell_grid[next_y][next_x].walls['right'] = False
        elif dx == -1:
            self.cell_grid[current_y][current_x].walls['right'] = False
            self.cell_grid[next_y][next_x].walls['left'] = False

        dy = current_y - next_y
        if dy == 1:
            self.cell_grid[current_y][current_x].walls['top'] = False
            self.cell_grid[next_y][next_x].walls['bottom'] = False
        elif dy == -1:
            self.cell_grid[current_y][current_x].walls['bottom'] = False
            self.cell_grid[next_y][next_x].walls['top'] = False

    # Check Wall is Present or Not (Solving Algorithm)
    def check_wall(self, x, y, side):
        return self.cell_grid[y][x].walls[side]
        
    # Check Cell Exist in Grid or Not (Solving Algorithm)
    def check_point(self, x, y):
        if (x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1):
            return False
    
        return self.pointer_grid[y][x]

    # Give All Possible Not Wall Neighbor Pointers (Solving Algorithm)
    def check_neighbor_pointers(self, x, y):
        neighbor_pointers = {}

        top = self.check_point(x, y - 1)
        right = self.check_point(x + 1, y)
        bottom = self.check_point(x, y + 1)
        left = self.check_point(x - 1, y)

        if top and not self.check_wall(x, y, "top"):
            neighbor_pointers["top"] = top
        
        if right and not self.check_wall(x, y, "right"):
            neighbor_pointers["right"] = right

        if bottom and not self.check_wall(x, y, "bottom"):
            neighbor_pointers["bottom"] = bottom

        if left and not self.check_wall(x, y, "left"):
            neighbor_pointers["left"] = left

        return neighbor_pointers

    # For movement of pointer
    def make_wall(self, current_x, current_y, next_x, next_y):

        dx = current_x - next_x

        if dx == 1:
            self.pointer_grid[current_y][current_x].connects["left"] = True
            self.pointer_grid[next_y][next_x].connects["right"] = True
        elif dx == -1:
            self.pointer_grid[current_y][current_x].connects["right"] = True
            self.pointer_grid[next_y][next_x].connects["left"] = True

        dy = current_y - next_y
        
        if dy == 1:
            self.pointer_grid[current_y][current_x].connects["top"] = True
            self.pointer_grid[next_y][next_x].connects["bottom"] = True
        elif dy == -1:
            self.pointer_grid[current_y][current_x].connects["bottom"] = True
            self.pointer_grid[next_y][next_x].connects["top"] = True

    # For movement of pointer (For Dead-End Fill)
    def remove_pointer_wall(self, current_x, current_y, next_x, next_y):

        dx = current_x - next_x

        if dx == 1:
            self.pointer_grid[current_y][current_x].connects["left"] = False
            self.pointer_grid[next_y][next_x].connects["right"] = False
        elif dx == -1:
            self.pointer_grid[current_y][current_x].connects["right"] = False
            self.pointer_grid[next_y][next_x].connects["left"] = False

        dy = current_y - next_y
        
        if dy == 1:
            self.pointer_grid[current_y][current_x].connects["top"] = False
            self.pointer_grid[next_y][next_x].connects["bottom"] = False
        elif dy == -1:
            self.pointer_grid[current_y][current_x].connects["bottom"] = False
            self.pointer_grid[next_y][next_x].connects["top"] = False