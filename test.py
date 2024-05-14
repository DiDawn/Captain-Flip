from tile_sprite import Tile
from board_pygame import Board
import ctypes
from parameters import *
from widgets import Button

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
pygame.init()
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_width, screen_height = screensize
screen = pygame.display.set_mode(screensize)

board = Board((screen_height * 2 // 3, screen_height * 2 // 3), 1)
tile = Tile((board.rect.w * 0.14, board.rect.h * 0.14),
            ('assets/tiles/cabin_boy.png', 'assets/tiles/monkey.png'))
tile.set_position((100, 100))
board.current_tile = tile
board.rect.topleft = (screen_width // 2 - board.rect.w // 2, screen_height // 2 - board.rect.h // 2)
board.minimise()
board.maximise()

flip_button = Button('assets/buttons/flip_button.png', convert_alpha=True)
flip_button = flip_button.resize(2)
flip_button.set_position((screen_width // 2 - flip_button.rect.w // 2, screen_height * 0.95 - flip_button.rect.h))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if flip_button.rect.collidepoint(event.pos):
                board.current_tile.flip()

        board.event_handler(event)

    board.update()
    screen.blit(board, board.rect.topleft)
    pygame.display.flip()
    if board.current_tile is None:
        board.current_tile = Tile((board.rect.w * 0.14, board.rect.h * 0.14),
                                  ('assets/tiles/cabin_boy.png', 'assets/tiles/monkey.png'))

    screen.blit(flip_button, flip_button.rect.topleft)

if __name__ == '__main__':
    pygame.quit()
