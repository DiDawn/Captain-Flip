import pygame as pygame
from surface_board import Tile


pygame.init()
screen = pygame.display.set_mode((640, 480))

group = pygame.sprite.Group()

tile = Tile((100, 100), ('assets/tiles/1.png', 'assets/tiles/2.png'))
tile.set_position((100, 100))
group.add(tile)


if __name__ == '__main__':
    pygame.quit()
