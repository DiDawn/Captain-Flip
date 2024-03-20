import pygame


class Image(pygame.Surface):
    def __init__(self, master: pygame.Surface, img: str | pygame.Surface, convert_alpha: bool = False):
        self.master = master
        self.convert2alpha = convert_alpha

        # load image if img is a string
        if type(img) is str:
            if not convert_alpha:
                self.image = pygame.image.load(img).convert()
            else:
                self.image = pygame.image.load(img).convert_alpha()

        elif type(img) is pygame.Surface:
            self.image = img
        else:
            raise Exception(f"img type should be str or pygame.Surface not {type(img)}")

        self.rect = self.image.get_rect()

        # if convert_alpha is False, we create a surface with no alpha channel
        if not convert_alpha:
            super().__init__((self.rect.width, self.rect.height))
        # otherwise this is used to set the sub surface(the one we will blit the actual image onto) to be transparent
        else:
            super().__init__((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)

        # blit the button image onto the sub surface which is our class
        self.blit(self.image, (0, 0))

    def resize(self, scale_factor: float | int):
        w, h = self.get_size()
        new_w, new_h = w * scale_factor, h * scale_factor
        img = pygame.transform.scale(self, [new_w, new_h])
        return Image(self.master, img, convert_alpha=self.convert2alpha)

    def set_position(self, position: tuple[float, float]):
        self.rect.topleft = position


class Button(Image):
    def __init__(self, master: pygame.Surface, img_path: str | pygame.Surface, call=None, convert_alpha: bool = False,
                 hashed: int = None):
        super().__init__(master, img_path, convert_alpha)

        self.call = call
        self.hover = False
        self.hashed = hash(self) if hashed is None else hashed

    def resize(self, scale_factor: float | int):
        w, h = self.get_size()
        new_w, new_h = w * scale_factor, h * scale_factor
        img = pygame.transform.scale(self, [new_w, new_h])
        return Button(self.master, img, call=self.call, convert_alpha=True, hashed=self.hashed)
