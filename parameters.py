import pygame

FIRST_MENU = 0
LOGIN_MENU = 1
REGISTER_MENU = 2
HOME_MENU = 3

# customs events for changing menus
CHANGE_TO_FIRST = pygame.USEREVENT + 1
CHANGE_TO_LOGIN = pygame.USEREVENT + 2
CHANGE_TO_REGISTER = pygame.USEREVENT + 3
CHANGE_TO_HOME = pygame.USEREVENT + 4
