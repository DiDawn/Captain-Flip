import pygame as pygame
from tile_sprite import Tile


pygame.init()
screen = pygame.display.set_mode((640, 480))

group = pygame.sprite.Group()

tile = Tile((100, 100), ('assets/tiles/cabin_boy.jpg', 'assets/tiles/monkey.jpg'))
tile.set_position((100, 100))
group.add(tile)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if tile.rect.collidepoint(event.pos):
                tile.flip()

    group.update()
    screen.fill((0, 0, 0))
    group.draw(screen)
    pygame.display.flip()


if __name__ == '__main__':
    pygame.quit()
