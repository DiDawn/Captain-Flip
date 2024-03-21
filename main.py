import pygame
import ctypes
from menus import LoginMenu, HomeMenu
from time import time


# init pygame module
pygame.init()

# get screen size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

background_colour = (0, 0, 0)
LOGIN_MENU = 0
HOME_MENU = 1

# define dimension of pygame screen (width,height)
screen = pygame.display.set_mode(screensize)

# Set the caption of the screen
pygame.display.set_caption('Captain FLip')

# Fill the background colour to the screen
screen.fill(background_colour)

# Update the display using flip
pygame.display.flip()

# init home_screen
login_menu = HomeMenu(screensize)
game_state = LOGIN_MENU

# Variable to keep our game loop running
running = True
screen.blit(login_menu, (0, 0))
time0 = time()
# game loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
        else:
            if game_state == LOGIN_MENU:
                login_menu.event_handler(event)

    # only update the parchment part since the background is static
    screen.blit(login_menu, login_menu.parchment_image.rect.topleft, login_menu.parchment_image.rect)
    pygame.display.flip()
    print(1/(time() - time0))
    time0 = time()
