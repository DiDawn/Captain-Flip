import pygame


class Image(pygame.Surface):
    def __init__(self, master: pygame.Surface, img: str | pygame.Surface, convert_alpha: bool = False):
        self.master = master
        self.convert2alpha = convert_alpha

        # load image
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

        if not convert_alpha:
            super().__init__((self.rect.width, self.rect.height))
        else:
            super().__init__((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)

        self.blit(self.image, (0, 0))

    def resize(self, scale_factor: float | int):
        w, h = self.get_size()
        new_w, new_h = w * scale_factor, h * scale_factor
        img = pygame.transform.scale(self, [new_w, new_h])
        return Image(self.master, img, convert_alpha=self.convert2alpha)

    def set_position(self, position: tuple[float, float]):
        self.rect.topleft = position


class Button(Image):
    def __init__(self, master: pygame.Surface, img_path: str | pygame.Surface, call=None, convert_alpha: bool = False):
        super().__init__(master, img_path, convert_alpha)

        self.call = call

    def resize(self, scale_factor: float | int):
        w, h = self.get_size()
        new_w, new_h = w * scale_factor, h * scale_factor
        img = pygame.transform.scale(self, [new_w, new_h])
        return Button(self.master, img, call=self.call, convert_alpha=True)
