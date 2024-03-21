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

    def rotate(self, a: float):
        img = pygame.transform.rotate(self, a)
        return Image(self.master, img, convert_alpha=self.convert2alpha)


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

    def rotate(self, a: float):
        img = pygame.transform.rotate(self, a)
        return Button(self.master, img, convert_alpha=self.convert2alpha)


class InputBox:
    def __init__(self, x, y, w, h, text='', under_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.under_text_color = pygame.Color((75, 75, 75))
        self.color_inactive = pygame.Color((0, 0, 0))
        self.color_active = pygame.Color((4, 54, 130))
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 48)
        self.under_text_font = pygame.font.Font(None, 48)
        self.txt_surface = self.font.render(text, True, self.color)
        self.under_text_surface = self.under_text_font.render(under_text, True, self.under_text_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 20)
        self.rect.w = width

    def draw(self, screen):
        # blit the under text
        if self.text == '' and self.active is False:
            screen.blit(self.under_text_surface, (self.rect.x + 10, self.rect.y + 10))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+10))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 5, border_radius=15)
