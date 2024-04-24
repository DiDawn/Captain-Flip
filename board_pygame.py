import pygame
from widgets import Image
from board import BoardManager


class Board(pygame.surface.Surface):
    def __init__(self, size: tuple[int, int], grid):

        self.size = size
        self.background_image = Image('assets/boards/board_1.png')
        self.scale_factor = size[0] / self.background_image.rect.w
        self.background_image = self.background_image.resize(scale_factor=self.scale_factor)

        # init the surface
        super().__init__(self.size)
        self.rect = self.get_rect()
        self.blit(self.background_image, (0, 0))

        # init the tiles group
        self.tiles_sprites = pygame.sprite.Group()

        self.current_tile = None
        self.current_tile_last_pos = (0, 0)

        self.grid = []
        for pos in grid:
            x, y = pos[0] * self.scale_factor, pos[1] * self.scale_factor
            self.grid.append(pygame.Rect(x, y, self.rect.w*0.14, self.rect.h*0.14))

    def set_position(self, position: tuple[int, int]):
        self.rect.topleft = position

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = self.relative_mouse_pos(pos)

            if self.current_tile is not None:
                if self.current_tile.rect.collidepoint((x, y)) and not self.current_tile.dragging:
                    self.current_tile.dragging = True
                    self.current_tile_last_pos = self.current_tile.rect.topleft

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            pos = self.relative_mouse_pos(pos)
            if self.current_tile is not None and self.current_tile.dragging:
                for rect in self.grid:
                    if rect.collidepoint(pos):
                        self.current_tile.rect.topleft = rect.topleft
                        break
                else:
                    self.current_tile.rect.topleft = self.current_tile_last_pos
                self.current_tile.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.current_tile is not None and self.current_tile.dragging:
                self.current_tile.update(self.rect.topleft)

    def update(self):
        self.blit(self.background_image, (0, 0))
        self.tiles_sprites.update(self.rect.topleft)
        self.tiles_sprites.draw(self)
        self.blit(self.current_tile.image, self.current_tile.rect.topleft)

    def relative_mouse_pos(self, pos):
        return pos[0] - self.rect.x, pos[1] - self.rect.y
