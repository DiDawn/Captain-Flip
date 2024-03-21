import pygame
import ctypes
from menus import LoginMenu, HomeMenu, FirstMenu
from time import time


# init pygame module
pygame.init()

# get screen size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

background_colour = (0, 0, 0)
FIRST_MENU = 0
LOGIN_MENU = 1
HOME_MENU = 2

# define dimension of pygame screen (width,height)
screen = pygame.display.set_mode(screensize)

# Set the caption of the screen
pygame.display.set_caption('Captain FLip')

# Fill the background colour to the screen
screen.fill(background_colour)

# Update the display using flip
pygame.display.flip()

# init home_screen
current_menu = LoginMenu(screensize)
game_state = LOGIN_MENU

# Variable to keep our game loop running
running = True
screen.blit(current_menu, (0, 0))
time0 = time()
fps_a = []
# game loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
        else:
            if game_state == LOGIN_MENU:
                current_menu.event_handler(event)
            if game_state == HOME_MENU or game_state == FIRST_MENU or game_state == LOGIN_MENU:
                # only update the parchment part since the background is static
                screen.blit(current_menu, current_menu.parchment_image.rect.topleft, current_menu.parchment_image.rect)
            else:
                screen.blit(current_menu, (0, 0))

    pygame.display.flip()

    # show fps
    delta = time() - time0
    fps = 1/delta if delta != 0 else 1200
    length = len(fps_a)
    if length != 1000:
        fps_a.append(fps)
    else:
        print(sum(fps_a)/length)
        fps_a = []
    time0 = time()
