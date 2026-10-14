import pygame
import os

pygame.init()

# Font Variables
font_24 = pygame.font.Font(None, 24)
font_35 = pygame.font.Font(None,35)
font_small_mini = pygame.font.Font(None, 25)

# Class For Text Blinking
def blit_text(screen, text, position, font, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Class For Tool Button
class ToolButton:

    def __init__(self, x, y, width, height, image_path, subtext, action_fun,args:tuple=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path) # Load an image
        self.image = pygame.transform.scale(self.image, (width-20, height-20))  # For Resize the image
        self.image_rect = self.image.get_rect() # Create a rectangle around the image
        self.image_rect.topleft = (x+10,y+10) # Set the position of the rectangle

        # Create an oval shape for subtext background
        self.font = font_small_mini
        self.subtext = subtext
        if len(subtext)<8:
            self.oval_rect = pygame.Rect(0, 0, 80, 30)  # Width and height of oval
            self.oval_rect.center = (self.rect.centerx, self.rect.top - 10)  # Position above button
        else:
            self.oval_rect = pygame.Rect(0, 0, len(subtext)*10, 30)  # Width and height of oval
            self.oval_rect.topleft = (self.rect.left - 30, self.rect.top - 10)  # Position above button

        self.button_color = (50,50,50)
        self.outline_color = (200,200,200)
        self.hover_color = (100,100,100)
        self.oval_color = (0,0,0)
        self.oval_border_color = (200,200,200)
        self.subtext_color = (255,255,255)

        self.action_fun = action_fun
        self.hovered = False
        self.args =args

    def draw(self, screen):

        # Change color if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.outline_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.hover_color, self.rect, 3, 10)
            
        # For Normal Button
        else:
            pygame.draw.rect(screen, self.button_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.outline_color, self.rect, 3, 10)
        
        # For Drawing Image
        screen.blit(self.image, self.image_rect.topleft)

        # Change color if hovered
        if self.hovered:
            # For Sub-Text
            pygame.draw.rect(screen, self.oval_color, self.oval_rect, 0, 10) # Draw oval background
            pygame.draw.rect(screen, self.oval_border_color, self.oval_rect, 2, 10) # Draw oval border
            subtext_surface = self.font.render(self.subtext, True, self.subtext_color) # Add subtext
            screen.blit(subtext_surface, (self.oval_rect.centerx - subtext_surface.get_width() // 2, self.oval_rect.centery - subtext_surface.get_height() //2))

    def handle_event(self, event):
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

         # Check if the button is clicked
        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN:
            if self.args:
                self.action_fun(*self.args)
            else:
                self.action_fun()

# For FileBrowserBox
class FileBrowserBox:
    def __init__(self, x, y, width, height, folder_path):
        self.rect = pygame.Rect(x+5, y+5, width-10, height-10)
        self.big_rect = pygame.Rect(x, y, width, height)
        self.folder_path = folder_path
        self.files = [file_name[:-5] for file_name in os.listdir(folder_path)]
        self.selected_file = None
        self.scroll_offset = 0
        self.font = font_24
        self.bg_color = (200,200,200)
        self.out_line_color = (100,100,100)
        self.hover_color = (150, 150, 250)
        self.click_color = (50, 200, 50)
        self.text_color = (0, 0, 0)
        self.file_height = 30
        self.scroll_bar_width = 10
        self.hovered_file = None

    def draw(self, screen):
        # Draw the box background
        pygame.draw.rect(screen, self.bg_color, self.big_rect,0,10)

        # Calculate visible files
        max_files = self.rect.height // self.file_height
        start_index = self.scroll_offset
        end_index = min(start_index + max_files, len(self.files))

        # Draw files in the box
        for index in range(start_index, end_index):
            file_name = self.files[index]
            file_rect = pygame.Rect(
                self.rect.x, self.rect.y + (index - start_index) * self.file_height,
                self.rect.width - self.scroll_bar_width, self.file_height
            )

            # Draw the file's background (hover and click visual effects handled in handle_event)
            if file_name == self.hovered_file:
                pygame.draw.rect(screen, self.hover_color, file_rect)
                
            if file_name == self.selected_file:
                pygame.draw.rect(screen, self.click_color, file_rect)

            # Draw the file name
            blit_text(screen,file_name,(file_rect.x + 5, file_rect.y + 5),self.font,self.text_color)

        # Draw the scroll bar
        total_files = len(self.files)
        if total_files > max_files:
            scroll_bar_rect = pygame.Rect(
                self.rect.x + self.rect.width - self.scroll_bar_width, self.rect.y,
                self.scroll_bar_width, self.rect.height
            )
            pygame.draw.rect(screen, (180, 180, 180), scroll_bar_rect)

            # Scroll bar handle
            scroll_ratio = self.scroll_offset / max(1, total_files - max_files)
            scroll_bar_height = max(20, self.rect.height * (max_files / total_files))
            scroll_bar_y = self.rect.y + scroll_ratio * (self.rect.height - scroll_bar_height)
            scroll_bar_handle_rect = pygame.Rect(
                self.rect.x + self.rect.width - self.scroll_bar_width, scroll_bar_y,
                self.scroll_bar_width, scroll_bar_height
            )
            pygame.draw.rect(screen, (100, 100, 100), scroll_bar_handle_rect)

        pygame.draw.rect(screen, self.out_line_color, self.big_rect,5,10)

    def scroll(self, direction):

        max_files = self.rect.height // self.file_height
        if direction == 'up' and self.scroll_offset > 0:
            self.scroll_offset -= 1
        elif direction == 'down' and self.scroll_offset < len(self.files) - max_files:
            self.scroll_offset += 1

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 4:  # Scroll up
                self.scroll('up')
            elif event.button == 5:  # Scroll down
                self.scroll('down')
            elif event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                max_files = self.rect.height // self.file_height
                start_index = self.scroll_offset
                end_index = min(start_index + max_files, len(self.files))

                for index in range(start_index, end_index):
                    file_rect = pygame.Rect(
                        self.rect.x, self.rect.y + (index - start_index) * self.file_height,
                        self.rect.width - self.scroll_bar_width, self.file_height
                    )
                    if file_rect.collidepoint(mouse_pos):
                        self.selected_file = self.files[index]

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            max_files = self.rect.height // self.file_height
            start_index = self.scroll_offset
            end_index = min(start_index + max_files, len(self.files))

            self.hovered_file = None
            for index in range(start_index, end_index):
                file_rect = pygame.Rect(
                    self.rect.x, self.rect.y + (index - start_index) * self.file_height,
                    self.rect.width - self.scroll_bar_width, self.file_height
                )
                if file_rect.collidepoint(mouse_pos):
                    self.hovered_file = self.files[index]
                
    def update(self):
        self.files = [file_name[:-5] for file_name in os.listdir(self.folder_path)]

# Class For Input-Text
class InputBox:

    def __init__(self,x,y,width,height,text=""):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.active = False
        self.font = font_35

        # Colors
        self.box_color = (25,25,25)
        self.font_color = (125,125,125)
        self.outline_color = (125,125,125)
        self.active_box_color = (100,100,100)
        self.active_font_color = (225,225,225)
        self.active_outline_color = (225,225,225)

    def draw(self,screen):
        if self.active:
            pygame.draw.rect(screen,self.active_box_color,self.rect,0,5)
            pygame.draw.rect(screen,self.active_outline_color,self.rect,3,5)
            pos = (self.rect.topleft[0]+10,self.rect.topleft[1]+7)
            blit_text(screen,self.text,pos,self.font,self.active_font_color)
        else:
            pygame.draw.rect(screen,self.box_color,self.rect,0,5)
            pygame.draw.rect(screen,self.outline_color,self.rect,3,5)
            pos = (self.rect.topleft[0]+10,self.rect.topleft[1]+7)
            blit_text(screen,self.text,pos,self.font,self.font_color)

    def handle_event(self,event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over the button
            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False

        if self.active and event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1] if self.text else ""
            elif event.key == pygame.K_SPACE:
                self.text += " "
            elif event.unicode.isalnum():
                self.text += event.unicode