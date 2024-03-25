import pygame


class Image(pygame.Surface):
    def __init__(self, master: pygame.Surface, img: str | pygame.Surface, convert_alpha: bool = False,
                 hashed: int = None):
        self.master = master
        self.convert2alpha = convert_alpha
        self.hashed = hash(self) if hashed is None else hashed

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
        super().__init__(master, img_path, convert_alpha, hashed=hashed)

        self.call = call
        self.hover = False

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


class Carousel(pygame.Surface):
    def __init__(self, size, screen_size, image_path: list[str], background_image: Image):
        super().__init__(size, pygame.SRCALPHA, 32)
        self.rect = self.get_rect()
        self.current_board = 0
        self.background_image = background_image

        self.images = [Image(self, img, convert_alpha=True) for img in image_path]
        self.buttons_side = []
        self.buttons_center = []

        self.side_carousel_next = {}
        self.side_carousel_previous = {}
        self.center_carousel_next = {}
        self.center_carousel_previous = {}

        # convert images to buttons
        self.convert_images2buttons()

        # resize images and buttons
        side_scale_factor = (screen_size[0] // 6) / self.buttons_side[0].rect.w
        self.resize_components(side_scale_factor, side_scale_factor * 2)

        # generate carousel
        self.generate_carousel()

        # set position of the first components
        self.span = screen_size[0] // 30

        self.left = self.buttons_side[-1]
        self.center = self.buttons_center[0]
        self.right = self.buttons_side[1]

        self.center_topleft = (screen_size[0] // 2 - self.center.rect.w // 2,
                               screen_size[1] // 1.6 - self.center.rect.h // 2)
        self.left_topleft = (self.center_topleft[0] - self.left.rect.w - self.span,
                             self.center_topleft[1] + (self.center.rect.h - self.left.rect.h) // 2)
        self.right_topleft = (self.center_topleft[0] + self.center.rect.w + self.span,
                              self.center_topleft[1] + (self.center.rect.h - self.right.rect.h) // 2)

        self.left.set_position(self.left_topleft)
        self.center.set_position(self.center_topleft)
        self.right.set_position(self.right_topleft)

        # blit the components
        self.blit(self.left, self.left.rect.topleft)
        self.blit(self.center, self.center.rect.topleft)
        self.blit(self.right, self.right.rect.topleft)

    def convert_images2buttons(self):
        for image in self.images:
            button = Button(self, image.image, convert_alpha=True)
            self.buttons_side.append(button)
            self.buttons_center.append(button)

    def resize_components(self, side_scale_factor: float | int, center_scale_factor: float | int):
        for i, button in enumerate(self.buttons_side):
            self.buttons_side[i] = button.resize(side_scale_factor)
        for i, button in enumerate(self.buttons_center):
            self.buttons_center[i] = button.resize(center_scale_factor)

    def generate_carousel(self):
        length = len(self.images)
        for i in range(length):
            button_side = self.buttons_side[i]
            button_center = self.buttons_center[i]
            i = i if i + 1 < length else -1
            self.side_carousel_next[button_side.hashed] = self.buttons_side[i+1]
            self.center_carousel_next[button_center.hashed] = self.buttons_center[i+1]

        # create previous carousel
        for i in range(length):
            button_side = self.buttons_side[i]
            button_center = self.buttons_center[i]
            i = i if i - 1 > -1 else length
            self.side_carousel_previous[button_side.hashed] = self.buttons_side[i-1]
            self.center_carousel_previous[button_center.hashed] = self.buttons_center[i-1]

    def next(self):
        self.current_board = self.current_board if self.current_board + 1 < len(self.buttons_side) else -1

        self.left = self.side_carousel_next[self.left.hashed]
        self.center = self.center_carousel_next[self.center.hashed]
        self.right = self.side_carousel_next[self.right.hashed]

        self.left.set_position(self.left_topleft)
        self.center.set_position(self.center_topleft)
        self.right.set_position(self.right_topleft)

        self.clean_background()
        self.blit(self.left, self.left.rect.topleft)
        self.blit(self.center, self.center.rect.topleft)
        self.blit(self.right, self.right.rect.topleft)

    def previous(self):
        self.current_board = self.current_board if self.current_board - 1 > -1 else len(self.buttons_side)

        self.left = self.side_carousel_previous[self.left.hashed]
        self.center = self.center_carousel_previous[self.center.hashed]
        self.right = self.side_carousel_previous[self.right.hashed]

        self.left.set_position(self.left_topleft)
        self.center.set_position(self.center_topleft)
        self.right.set_position(self.right_topleft)

        self.clean_background()
        self.blit(self.left, self.left.rect.topleft)
        self.blit(self.center, self.center.rect.topleft)
        self.blit(self.right, self.right.rect.topleft)

    def clean_background(self):
        w = self.left.rect.w + self.center.rect.w + self.right.rect.w + 2 * self.span
        h = self.center.rect.h
        x, y = self.center_topleft
        x -= self.left.rect.w
        self.blit(self.background_image, (x, y), (x, y, w, h))

    def set_position(self, pos):
        self.rect.topleft = pos
