import ctypes
from menus import LoginMenu, HomeMenu, FirstMenu, GameModeMenu, ChooseBoardMenu, RulesMenu, StatsMenu, ChooseNumberOfPlayersMenu, LoginGuestsMenu, EndGameMenu
from time import time
from parameters import *
from player import Player
from game import Game
from database import Database

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
player = Player('ok')

# init menu
first_menu = FirstMenu(screensize)
login_menu = LoginMenu(screensize, "login", player=player)
register_menu = LoginMenu(screensize, "register")
home_menu = HomeMenu(screensize)
game_mode_menu = GameModeMenu(screensize)
choose_board_menu = ChooseBoardMenu(screensize)
rules_menu = RulesMenu(screensize)
stats_menu = StatsMenu(screensize)
choose_number_of_players_menu = ChooseNumberOfPlayersMenu(screensize)
login_guests_menu = LoginGuestsMenu(screensize, 0)
end_game_menu = EndGameMenu(screensize)

game = None
players = [player]

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
    STATS_MENU: stats_menu,
    CHOOSE_NUMBER_OF_PLAYERS_MENU: choose_number_of_players_menu,
    LOGIN_GUESTS_MENU: login_guests_menu,
    END_GAME_MENU: end_game_menu
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
    clock.tick(60)
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

        elif event.type == CHANGE_TO_CHOOSE_NUMBER_OF_PLAYERS:
            game_state = CHOOSE_NUMBER_OF_PLAYERS_MENU
            current_menu = menus[CHOOSE_NUMBER_OF_PLAYERS_MENU]

        elif event.type == CHANGE_TO_LOGIN_GUESTS:
            login_guests_menu.n = event.number
            game_state = LOGIN_GUESTS_MENU
            current_menu = menus[LOGIN_GUESTS_MENU]

        elif event.type == CHANGE_TO_CHOOSE_BOARD:
            if event.gamemode == "single_player":
                game_state = CHOOSE_BOARD_MENU
                current_menu = menus[CHOOSE_BOARD_MENU]
            elif event.gamemode == "multi_player":
                n = len(players)
                players = [player]
                players.extend(event.guests[n-1:])
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
            player = Player('ok')
            stats_menu.update_stats(player.stats)

        elif event.type == START_GAME:
            for pl in players:
                pl.reset()
            game = Game(screen, screensize, event.board_number, players)
            current_menu = game

        elif event.type == CHANGE_TO_END_GAME:
            end_game_menu.show_results(event.players)
            players2 = event.players[:]
            players2.sort(key=lambda x: x.gold, reverse=True)
            winner = players2[0]
            if winner == player:
                Database.add_victory("database.csv", player.username)
                player.stats = (str(int(player.stats[0]) + 1), player.stats[1], player.stats[2])
            else:
                for pl in players2:
                    if pl == player:
                        if pl.gold == winner.gold:
                            Database.add_draw("database.csv", player.username)
                            player.stats = (player.stats[0], str(int(player.stats[1]) + 1), player.stats[2])
                        else:
                            Database.add_defeat("database.csv", player.username)
                            player.stats = (player.stats[0], player.stats[1], str(int(player.stats[2]) + 1))
            stats_menu.update_stats(player.stats)

            game_state = END_GAME_MENU
            current_menu = end_game_menu

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
