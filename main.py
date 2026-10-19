# Entry Point Programm for this Project, Connects all modules together

# External Modules
import pygame

# Internal Modules
from maze import Grid
from tools import ToolButton, FileBrowserBox, InputBox, blit_text
import saver_loader as SL

# Import Maze Generation Algorithm
from algorithm import depth_first_search, hunt_and_kill
# Import Maze Solver Algorithm
from algorithm import random_mouse, dead_end_fill, right_hand_follower, left_hand_follower, a_star, dijkstra_algorithm
# Import Helper Function for Maze Solver Algorithm
from algorithm import explore_maze, initialize_a_star, initialize_dijkstra

pygame.init()       # Initialize Pygame components

# For Screen/Window Basic
WIDTH = 1000
HEIGHT = 600
RES = WIDTH,HEIGHT
win = pygame.display.set_mode(RES)
pygame.display.set_caption("The Maze - Dip Parmar")
clock = pygame.time.Clock()
FPS = 60

# Global Variables

# Font Objects
font_small_mini = pygame.font.Font(None, 25)
font_small_medium = pygame.font.Font(None, 33)
font_small = pygame.font.Font(None, 45)
font_medium = pygame.font.Font(None, 55)

# Colors
BG_Color = (50, 50, 50)
TOOL_Bar_Color = (100, 140, 200)
TOOL_Bar_Mid_Color = (37, 76, 139)
MAZE_Box_Border_Color = (97, 136, 199)

# Define a color with an alpha value (RGBA)
transparent_color = (0, 0, 0, 150)  # RGB Color with 50% transparency

# Create a surface with transparency
transparent_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
transparent_surface.fill(transparent_color)

# UI related Varibles
save_load_screen = None

# Maze Varibles

# tile size range from 10 to 50 (10,25,50)
Tile_Size = 50
grid_obj = Grid(25, 25, 800, 550, Tile_Size, MAZE_Box_Border_Color)

# Algorithm Function Mapping
gen_algorithm_map = {
    "DFS": depth_first_search,  # Depth-First Search
    "HAK": hunt_and_kill        # Hunt and Kill
}

solve_algorithm_map = {
    "RMA": random_mouse,            # Random Mouse
    "DEF": dead_end_fill,           # Dead-End Fill
    "LHF": left_hand_follower,      # Left-Hand Follower
    "RHF": right_hand_follower,     # Right-Hand Follower
    "AS": a_star,                   # A Star
    "DA": dijkstra_algorithm        # Dijkstra
}

# Utility Functions for Each tool of toolbar

# For Save pop-up
def save_menu_fun():
    global save_load_screen
    save_load_screen = "save"

# For Open pop-up
def open_menu_fun():
    global save_load_screen
    save_load_screen = "open"

# For Deleting Entire Maze
def delete_fun():
    global grid_obj
    print("Delete Function Called")
    grid_obj = Grid(25, 25, 800, 550, Tile_Size, MAZE_Box_Border_Color)

# For Reset Solved Path by Solving Algoritm also Stop Solving Algorithm
def reset_fun():
    grid_obj.reset_solve()
    print("Reset Function Called.")

# Combined Function for all maze genration algorithm
def gen_algorithm_fun(algorithm_name):
    global grid_obj
    grid_obj.gen_algo_is_running = True
    grid_obj.gen_algorithm = gen_algorithm_map.get(algorithm_name)

# Combined Function for all maze solving algorithm
def solve_algorithm_fun(algorithm_name):
    global grid_obj

    # Only Run Logic if Maze is generated
    if grid_obj.is_maze_Generated:

        # Rest Existing Path and algorithm
        reset_fun()
        grid_obj.solve_algo_is_running = True

        # Initialization Function Calling Condition for some of the Algorithms

        # For dead-end fill algorithm
        if (algorithm_name == "DEF"):
            # Make All Pointer Visited and in_path
            explore_maze(grid_obj)

        # For A-Star algorithm
        elif (algorithm_name == "AS"):
            # Calculate and Store Score for each cell
            initialize_a_star(grid_obj)

        # For Dijkstra's algorithm
        elif (algorithm_name == "DA"):
            # Calculate and Store Distance for each cell
            initialize_dijkstra(grid_obj)

        # Assign Algorithm Funtion
        grid_obj.solve_algorithm = solve_algorithm_map.get(algorithm_name)

    # Warning if maze is not genrated
    else:
        print("Generate or Load Maze First")

# For Zoom-In or make maze grid bigger
def expand_menu_fun():
    global Tile_Size

    if Tile_Size == 10:
        Tile_Size = 25
        delete_fun()

    elif Tile_Size == 25:
        Tile_Size = 50
        delete_fun()

    else:
        print("Out of range")
    
# For Zoom-Out or make maze grid smaller
def shrink_menu_fun():
    global Tile_Size

    if Tile_Size == 50:
        Tile_Size = 25
        delete_fun()

    elif Tile_Size == 25:
        Tile_Size = 10
        delete_fun()

    else:
        print("Out of range")

# For Close Mini-Window of Save-Load Screen
def close_fun():
    global save_load_screen
    save_load_screen = None

# For Finally Save The File
def save_fun():
    global save_load_screen
    SL.save_maze(input_box.text, grid_obj)
    save_load_screen = None
    filelist_box.update()

# For Finally Open The File
def open_fun():
    global save_load_screen
    delete_fun()
    grid_obj.is_maze_Generated = SL.load_maze(filelist_box.selected_file, grid_obj)
    save_load_screen = None

# Objects For UI
# For Load
close_button_1 = ToolButton(600,105,40,40,"img\\close.png","Close",close_fun)
open_button = ToolButton(470,430,60,60,"img\\folder.png","Open",open_fun)
filelist_box = FileBrowserBox(370,180,260,240,"MazeGrids")

# For Save
close_button = ToolButton(600,205,40,40,"img\\close.png","Close",close_fun)
input_box = InputBox(370,280,260,40,"MyMaze")
save_button = ToolButton(470,330,60,60,"img\\diskette.png","Save",save_fun)

# For Tool Button(Tool) List
tool_buttons = []

# Row - 1 
# Save Tool Button
tool_buttons.append(ToolButton(860,70,50,50,"img\\diskette.png","Save",save_menu_fun))
# Open Tool Button
tool_buttons.append(ToolButton(920,70,50,50,"img\\folder.png","Open",open_menu_fun))

# Row - 2
# Delete Tool Button
tool_buttons.append(ToolButton(860,130,50,50,"img\\delete.png","Delete",delete_fun))
# Reset Tool Button
tool_buttons.append(ToolButton(920,130,50,50,"img\\reset.png","Reset",reset_fun))

# Row - 3
# Zoom In Tool Button
tool_buttons.append(ToolButton(860,190,50,50,"img\\zoom-in.png","Expand",expand_menu_fun))
# Zoom Out Tool Button
tool_buttons.append(ToolButton(920,190,50,50,"img\\zoom-out.png","Shrink",shrink_menu_fun))

# Row - 4
# DFS Tool Button
tool_buttons.append(ToolButton(860,290,50,50,"img\\DFS.png","DFS",lambda: gen_algorithm_fun("DFS")))
# Hunt and Kill Tool Button
tool_buttons.append(ToolButton(920,290,50,50,"img\\huntandkill.png","Hunt & Kill",lambda: gen_algorithm_fun("HAK")))

# Row - 5
# Random Mouse Algorithm Button
tool_buttons.append(ToolButton(860,395,50,50,"img\\randommouse.png","Random",lambda: solve_algorithm_fun("RMA")))
# Dead-End Fill Algorithm Button
tool_buttons.append(ToolButton(920,395,50,50,"img\\deadendfill.png","DeadEnd-Fill",lambda: solve_algorithm_fun("DEF")))

# Row - 6
# Left-Hand Follower Algorithm Button
tool_buttons.append(ToolButton(860,455,50,50,"img\\lefthand.png","Left Hand",lambda: solve_algorithm_fun("LHF")))
# Right-Hand Follower Algorithm Button
tool_buttons.append(ToolButton(920,455,50,50,"img\\righthand.png","Right Hand",lambda: solve_algorithm_fun("RHF")))

# Row - 7
# A-star Algorithm Button
tool_buttons.append(ToolButton(860,515,50,50,"img\\astar.png","A Star",lambda: solve_algorithm_fun("AS")))
# Dijkstra Algorithm Button
tool_buttons.append(ToolButton(920,515,50,50,"img\\dijkstra.png","Dijkstra",lambda: solve_algorithm_fun("DA")))

# Draw things on Pygame screen
def draw_win(sc: pygame.Surface):
    # For Background Color
    sc.fill(BG_Color)        

    # Main Maze Grid
    grid_obj.draw(sc)

    # For Tool Bar
    pygame.draw.rect(sc, TOOL_Bar_Color, (850, 25, 130, 550), 0, 10)
    # For Middle Differen Tool Bar BG For Generation Algorithm
    pygame.draw.rect(sc, TOOL_Bar_Mid_Color, (850, 250, 130, 100), 0, 10)

    # For Tool Bar Texts
    blit_text(win,"Tools",(875,35),font_small,(255,255,255))
    blit_text(win,"Generator",(860,260),font_small_medium,(255,255,255))
    blit_text(win,"Solver",(870,360),font_small,(255,255,255))

    # For Tools Button
    for button in tool_buttons:
        button.draw(win)

    # For Custom Pop-up
    if save_load_screen:
        # For Transparent Background
        win.blit(transparent_surface,(0,0))

        # For Save Pop-up
        if save_load_screen == "save":
            # For Background Box
            pygame.draw.rect(win,(50,50,50),(350,200,300,200),0,20)
            pygame.draw.rect(win,(200,200,200),(350,200,300,200),5,20)
            pygame.draw.rect(win,(100,100,100),(350,200,300,50),0,border_top_left_radius=20,border_top_right_radius=20)

            # For Texts Drawing
            blit_text(win,"Save Menu",(365,215),font_small,(255,255,255))
            blit_text(win,"Enter File Name:",(375,260),font_small_mini,(220,220,220))

            # For Objects Draw on screen
            input_box.draw(win)             # For Input Box Draw
            close_button.draw(win)          # For Close Button Draw
            save_button.draw(win)           # For Save Button Draw

        # For Open Pop-up
        else:
            # For Background Box
            pygame.draw.rect(win,(50,50,50),(350,100,300,400),0,20)
            pygame.draw.rect(win,(200,200,200),(350,100,300,400),5,20)
            pygame.draw.rect(win,(100,100,100),(350,100,300,50),0,border_top_left_radius=20,border_top_right_radius=20)
            
            # For Texts Drawing
            blit_text(win,"Open Menu",(365,115),font_small,(255,255,255))
            blit_text(win,"Select File To Open:",(375,160),font_small_mini,(220,220,220))

            # For Objects Draw on screen
            close_button_1.draw(win)            # For Close Button Draw
            filelist_box.draw(win)              # For Filelist Box Draw
            open_button.draw(win)               # For Open Button Draw

# Handle User-interations(input) events
def handle_events(event: pygame.event.Event):

    # Handle events for pop-ups
    if save_load_screen:

        # Handle Save pop-up Events
        if save_load_screen == "save":
            close_button.handle_event(event)        # close button event handling
            save_button.handle_event(event)         # save button event handling
            input_box.handle_event(event)           # input box event handling

        # Handle Open pop-up Events
        else:
            close_button_1.handle_event(event)      # close button event handling
            open_button.handle_event(event)         # open button event handling
            filelist_box.handle_event(event)        # file list box event handling

    # General events
    else:
        # Maze Grid Event Handling(only for manual solve)
        grid_obj.handle_events(event)

        # For Tool Button Events
        for button in tool_buttons:
            button.handle_event(event)

# Main Entry function for the module and whole project
def main():

    # For Gameloop
    while True:

        # For Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # For Handling Maze Events
            handle_events(event)

        # For Drawing Maze On Window
        draw_win(win)

        # For Update Display
        pygame.display.flip()
        clock.tick(FPS)

# File Run It self not from other file
if __name__=="__main__":
    main()

    pygame.quit()       # close pygame window
    exit()              # exit terminal where code is running