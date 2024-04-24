import pygame as pygame
from tile_sprite import Tile
from board_pygame import Board
import ctypes
from parameters import *


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))

group = pygame.sprite.Group()
board = Board((1080*2//3, 1080*2//3), BOARD_A_GRID)
tile = Tile((board.rect.w * 0.14, board.rect.h * 0.14),
            ('assets/tiles/cabin_boy.png', 'assets/tiles/monkey.png'))
tile.set_position((100, 100))
board.current_tile = tile
board.rect.topleft = (1920 // 2 - board.rect.w // 2, 1080 // 2 - board.rect.h // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            board.event_handler(event)

    board.update()
    screen.blit(board, board.rect.topleft)
    pygame.display.flip()

if __name__ == '__main__':
    pygame.quit()
