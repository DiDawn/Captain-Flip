import pygame
import ctypes
from menus import LoginMenu, HomeMenu, FirstMenu
from time import time
from parameters import *


# init pygame module
pygame.init()

# get screen size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# define dimension of pygame screen (width,height)
screen = pygame.display.set_mode(screensize)

# Set the caption of the screen
pygame.display.set_caption('Captain FLip')

# Update the display using flip
pygame.display.flip()

# init menus
first_menu = FirstMenu(screensize)
login_menu = LoginMenu(screensize, "login")
register_menu = LoginMenu(screensize, "register")
home_menu = HomeMenu(screensize)

# create dictionary to store menus
menus = {
    FIRST_MENU: first_menu,
    LOGIN_MENU: login_menu,
    REGISTER_MENU: register_menu,
    HOME_MENU: home_menu
}

game_state = FIRST_MENU
current_menu = FirstMenu(screensize)

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
        # check for custom events
        elif event.type == CHANGE_TO_FIRST:
            game_state = FIRST_MENU
            current_menu = menus[FIRST_MENU]
        elif event.type == CHANGE_TO_LOGIN:
            game_state = LOGIN_MENU
            current_menu = menus[LOGIN_MENU]
        elif event.type == CHANGE_TO_REGISTER:
            game_state = REGISTER_MENU
            current_menu = menus[REGISTER_MENU]
        elif event.type == CHANGE_TO_HOME:
            game_state = HOME_MENU
            current_menu = menus[HOME_MENU]

        else:
            current_menu.event_handler(event)

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
