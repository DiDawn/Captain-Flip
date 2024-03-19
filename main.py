import pygame
import ctypes
from menus import HomeMenu

# init pygame module
pygame.init()

# get screen size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

background_colour = (0, 0, 0)
HOME_MENU = 0

# define dimension of pygame screen (width,height)
screen = pygame.display.set_mode(screensize)

# Set the caption of the screen
pygame.display.set_caption('Captain FLip')

# Fill the background colour to the screen
screen.fill(background_colour)

# Update the display using flip
pygame.display.flip()

# init home_screen
home_menu = HomeMenu(screensize)
game_state = HOME_MENU

# Variable to keep our game loop running
running = True

# game loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
        else:
            if game_state == HOME_MENU:
                home_menu.event_handler(event)

    screen.blit(home_menu, (0, 0))
    pygame.display.flip()
