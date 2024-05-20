import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], images: tuple[str, str], tile_manager, pos: tuple[int, int] = (0, 0)):
        self.size = size
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.dragging = False
        self.minimised = False
        self.tile_manager = tile_manager
        self.pos = pos
        self.x, self.y = pos

        super().__init__()

        # init the variable that will track the face of the tile
        self.face = 1
        self.flipped = False

        # load both faces of the tile
        self.face1 = pygame.image.load(images[0])
        self.face2 = pygame.image.load(images[1])

        # resize the faces
        self.face1 = pygame.transform.scale(self.face1, size)
        self.face2 = pygame.transform.scale(self.face2, size)
        self.minimised_face1 = pygame.transform.scale(self.face1, (size[0] // 2, size[1] // 2))
        self.minimised_face2 = pygame.transform.scale(self.face2, (size[0] // 2, size[1] // 2))

        # set the face of the tile
        self.image = self.face1

    def set_position(self, position: tuple[int, int]):
        self.rect.topleft = position

    def set_pos_in_grid(self, pos: tuple[int, int]):
        self.x, self.y = pos
        self.pos = pos

    def flip(self):
        if not self.flipped:
            self.image = self.face2 if self.face == 1 else self.face1
            self.face = 1 if self.face == 2 else 2
            self.flipped = True
            self.tile_manager.flip()

    def monkey_flip(self):
        self.image = self.face2 if self.face == 1 else self.face1
        self.face = 1 if self.face == 2 else 2
        self.flipped = True
        self.tile_manager.flip()

    def update(self, board_pos: tuple[int, int], minimised: bool = False):
        if self.dragging:
            pos = pygame.mouse.get_pos()
            x, y = pos[0] - board_pos[0], pos[1] - board_pos[1]
            self.rect.topleft = (x - self.size[0] // 2, y - self.size[1] // 2)
        if minimised and not self.minimised:
            x, y = self.rect.topleft
            self.rect.topleft = (x // 2, y // 2)
            self.rect.size = (self.size[0] // 2, self.size[1] // 2)
            self.image = self.minimised_face2 if self.face == 2 else self.minimised_face1
            self.minimised = True
        elif not minimised and self.minimised:
            x, y = self.rect.topleft
            self.rect.topleft = (x * 2, y * 2)
            self.rect.size = self.size
            self.image = self.face2 if self.face == 2 else self.face1
            self.minimised = False
