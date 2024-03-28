import pygame
from widgets import Image


class Board(pygame.surface.Surface):
    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.background_image = Image('assets/boards/board_1.png')
        self.background_image = self.background_image.resize(size[0] / self.background_image.rect.w)

        # init the surface
        super().__init__(self.size)
        self.rect = self.get_rect()
        self.blit(self.background_image, (0, 0))

        # init the tiles group
        self.tiles_sprites = pygame.sprite.Group()

        self.current_tile = None

    def set_position(self, position: tuple[int, int]):
        self.rect.topleft = position

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.current_tile is not None:
                if self.current_tile.rect.collidepoint(pos) and not self.current_tile.dragging:
                    self.current_tile.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.current_tile is not None and self.current_tile.dragging:
                self.current_tile.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.current_tile is not None and self.current_tile.dragging:
                self.current_tile.update()

    def update(self):
        self.blit(self.background_image, (0, 0))
        self.tiles_sprites.update()
        self.tiles_sprites.draw(self)
        self.blit(self.current_tile.image, self.current_tile.rect.topleft)
