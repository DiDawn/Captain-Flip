import pygame
from widgets import Image
from board import BoardManager
from parameters import BOARDS_GRID


class Board(pygame.surface.Surface):
    def __init__(self, size: tuple[int, int], board_number):
        self.board_manager = BoardManager(board_number)

        self.size = size
        self.background_image = Image(f'assets/boards/board_{board_number + 1}.png')
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
        self.columns_positions = []
        x_list = []
        for pos in BOARDS_GRID[board_number]:
            x, y = pos[0] * self.scale_factor, pos[1] * self.scale_factor
            x_list.append(x)
            self.grid.append(pygame.Rect(x, y, self.rect.w*0.14, self.rect.h*0.14))

        # approximate the x positions of the columns
        x_list.sort()
        i = 0
        for column in self.board_manager.columns:
            average_pos = sum(x_list[i:i+column.length]) // column.length
            self.columns_positions.append(average_pos)
            i += column.length

        self.columns_rects = [[] for _ in range(5)]
        for rect in self.grid:
            nearest_column = min(self.columns_positions, key=lambda x: abs(x - rect.x))
            column_number = self.columns_positions.index(nearest_column)
            self.columns_rects[column_number].append(rect)
        for i, column in enumerate(self.columns_rects):
            column.sort(key=lambda x: x.y, reverse=True)
            self.columns_rects[i] = column

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
                    if rect.collidepoint(pos) :
                        nearest_column = min(self.columns_positions, key=lambda x: abs(x - rect.x))
                        column_number = self.columns_positions.index(nearest_column)

                        empty_tiles = self.board_manager.get_empty_tiles()
                        if not all(c is None for c in empty_tiles):
                            if rect.topleft == self.columns_rects[column_number][self.board_manager.get_empty_tiles()[column_number]].topleft:
                                self.current_tile.rect.topleft = rect.topleft
                                # update the board manager
                                if self.board_manager.insert_tile(column_number, self.current_tile):
                                    self.tiles_sprites.add(self.current_tile)
                                    self.current_tile.dragging = False
                                    self.current_tile = None
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
        if self.current_tile is not None:
            self.blit(self.current_tile.image, self.current_tile.rect.topleft)

    def relative_mouse_pos(self, pos):
        return pos[0] - self.rect.x, pos[1] - self.rect.y
