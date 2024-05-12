import ctypes
from menus import LoginMenu, HomeMenu, FirstMenu, GameModeMenu, ChooseBoardMenu, RulesMenu, StatsMenu
from time import time
from parameters import *
from player import Player

# init pygame module
pygame.init()

# get screen size
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()  # corrects the resolution of the screen
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# define dimension of pygame screen (width,height)
screen = pygame.display.set_mode(screensize)

# Set the caption of the screen
pygame.display.set_caption('Captain FLip')

# Update the display using flip
pygame.display.flip()

# init player
player = Player(1)

# init menu
first_menu = FirstMenu(screensize)
login_menu = LoginMenu(screensize, "login", player=player)
register_menu = LoginMenu(screensize, "register")
home_menu = HomeMenu(screensize)
game_mode_menu = GameModeMenu(screensize)
choose_board_menu = ChooseBoardMenu(screensize)
rules_menu = RulesMenu(screensize)
stats_menu = StatsMenu(screensize)

# load and start music
pygame.mixer.music.load('assets/music/sot_bo.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# create dictionary to store menus
menus = {
    FIRST_MENU: first_menu,
    LOGIN_MENU: login_menu,
    REGISTER_MENU: register_menu,
    HOME_MENU: home_menu,
    GAME_MODE_MENU: game_mode_menu,
    CHOOSE_BOARD_MENU: choose_board_menu,
    RULES_MENU: rules_menu,
    STATS_MENU: stats_menu
}

game_state = LOGIN_MENU
current_menu = FirstMenu(screensize)
# initialize pygame clock
clock = pygame.time.Clock()
# Variable to keep our game loop running
running = True
screen.blit(current_menu, (0, 0))
time0 = time()
fps_a = []
# game loop
while running:
    # tick the clock
    #clock.tick(60)
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
        elif event.type == CHANGE_TO_GAMEMODE:
            game_state = GAME_MODE_MENU
            current_menu = menus[GAME_MODE_MENU]
        elif event.type == CHANGE_TO_CHOOSE_BOARD:
            game_state = CHOOSE_BOARD_MENU
            current_menu = menus[CHOOSE_BOARD_MENU]
        elif event.type == CHANGE_TO_RULES:
            game_state = RULES_MENU
            current_menu = menus[RULES_MENU]
        elif event.type == CHANGE_TO_STATS:
            game_state = STATS_MENU
            current_menu = menus[STATS_MENU]
        elif event.type == UPDATE_STATS:
            player = login_menu.player
            stats_menu.player = player
            stats_menu.update_stats(player.stats)
        elif event.type == RESET_PLAYER:
            player = Player()
            stats_menu.update_stats(player.stats)

        else:
            current_menu.event_handler(event)

    screen.blit(current_menu, (0, 0))

    pygame.display.flip()

    # show fps
    delta = time() - time0
    fps = 1 / delta if delta != 0 else 1200
    length = len(fps_a)
    if length != 1000:
        fps_a.append(fps)
    else:
        print(sum(fps_a) / length)
        fps_a = []
    time0 = time()
