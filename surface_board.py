import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], images: tuple[str, str]):
        self.size = size
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()

        super().__init__()

        # init the variable that will track the face of the tile
        self.face = 1

        # load both faces of the tile
        self.face1 = pygame.image.load(images[0])
        self.face2 = pygame.image.load(images[1])

        # resize the faces
        self.face1 = pygame.transform.scale(self.face1, size)
        self.face2 = pygame.transform.scale(self.face2, size)

        # set the face of the tile
        self.image = self.face1

    def set_position(self, position: tuple[int, int]):
        self.rect.topleft = position

    def flip(self):
        self.image = self.face2 if self.face == 1 else self.face1
        self.face = 1 if self.face == 2 else 2

    def update(self):
        pass
