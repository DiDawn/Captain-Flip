import pygame


class Image(pygame.Surface):
    def __init__(self, img: str | pygame.Surface, convert_alpha: bool = False,
                 hashed: int = None):
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
        return Image(img, convert_alpha=self.convert2alpha)

    def set_position(self, position: tuple[float, float]):
        self.rect.topleft = position

    def rotate(self, a: float):
        img = pygame.transform.rotate(self, a)
        return Image(img, convert_alpha=self.convert2alpha)


class Button(Image):
    def __init__(self, img_path: str | pygame.Surface, call=None, convert_alpha: bool = False,
                 hashed: int = None):
        super().__init__(img_path, convert_alpha, hashed=hashed)

        self.call = call
        self.hover = False

    def resize(self, scale_factor: float | int):
        w, h = self.get_size()
        new_w, new_h = w * scale_factor, h * scale_factor
        img = pygame.transform.scale(self, [new_w, new_h])
        return Button(img, call=self.call, convert_alpha=True, hashed=self.hashed)

    def rotate(self, a: float):
        img = pygame.transform.rotate(self, a)
        return Button(img, convert_alpha=self.convert2alpha)


class InputBox:
    def __init__(self, x, y, w, h, text='', under_text='', background_image: Image = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.under_text_color = pygame.Color((75, 75, 75))
        self.color_inactive = pygame.Color((0, 0, 0))
        self.color_active = pygame.Color((4, 54, 130))
        self.color_wrong_input = pygame.Color((255, 0, 0))
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 48)
        self.under_text_font = pygame.font.Font(None, 48)
        self.txt_surface = self.font.render(text, True, self.color)
        self.under_text = under_text
        self.under_text_surface = self.under_text_font.render(under_text, True, self.under_text_color)
        self.active = False
        self.wrong_input = False

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
                elif event.key == pygame.K_TAB:
                    pass
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
        if self.wrong_input and not self.active:
            pygame.draw.rect(screen, self.color_wrong_input, self.rect, 5, border_radius=15)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 5, border_radius=15)

    def update_text_surface(self):
        self.txt_surface = self.font.render(self.text, True, self.color)

    def change_under_text(self, text: str):
        self.under_text = text
        self.under_text_surface = self.under_text_font.render(text, True, self.under_text_color)


class Carousel(pygame.Surface):
    def __init__(self, size, screen_size, image_path: list[str], background_image: Image):
        super().__init__(size, pygame.SRCALPHA, 32)
        self.rect = self.get_rect()
        self.current_board = 0
        self.background_image = background_image
        self.swiping = False
        self.swipe_mode = None
        self.max_swipe_state = 35
        self.swipe_state = 0
        self.swiping_images = []
        self.side_alpha = 150

        self.images = [Image(img, convert_alpha=True) for img in image_path]
        self.buttons_side = []
        self.buttons_center = []

        self.side_carousel_next = {}
        self.side_carousel_previous = {}
        self.center_carousel_next = {}
        self.center_carousel_previous = {}

        # convert images to buttons
        self.convert_images2buttons()

        # resize images and buttons
        self.side_scale_factor = (screen_size[0] // 6) / self.buttons_side[0].rect.w
        self.center_scale_factor = self.side_scale_factor * 2
        self.resize_components(self.side_scale_factor, self.center_scale_factor)

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
            button = Button(image.image, convert_alpha=True)
            button_side = Button(image.image, convert_alpha=True)
            button_side.set_alpha(self.side_alpha)
            self.buttons_side.append(button_side)
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
        self.current_board = self.current_board + 1 if self.current_board + 1 < len(self.buttons_side) else 0
        print(self.current_board)

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
        self.current_board = self.current_board - 1 if self.current_board - 1 > -1 else len(self.buttons_side) - 1
        print(self.current_board)

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
        x -= self.left.rect.w + self.span
        self.blit(self.background_image, (x, y), (x, y, w, h))

    def set_position(self, pos):
        self.rect.topleft = pos

    def swipe_image(self, image, mode: str):
        swipe_state = self.swipe_state / self.max_swipe_state
        match mode:
            case 'left_side2center':
                scale_range = abs(1 - self.center_scale_factor / self.side_scale_factor)
                scale_factor = 1 + scale_range * swipe_state
                alpha_range = 255 - self.side_alpha
                alpha = self.side_alpha + alpha_range * swipe_state
                distance_x = abs(self.center_topleft[0] - self.left_topleft[0])
                distance_y = abs(self.center_topleft[1] - self.left_topleft[1])
                new_x = self.left_topleft[0] + distance_x * swipe_state
                new_y = self.left_topleft[1] - distance_y * swipe_state
            case 'right_side2center':
                scale_range = abs(1 - self.center_scale_factor / self.side_scale_factor)
                scale_factor = 1 + scale_range * swipe_state
                alpha_range = 255 - self.side_alpha
                alpha = self.side_alpha + alpha_range * swipe_state
                distance_x = abs(self.center_topleft[0] - self.right_topleft[0])
                distance_y = abs(self.center_topleft[1] - self.right_topleft[1])
                new_x = self.right_topleft[0] - distance_x * swipe_state
                new_y = self.right_topleft[1] - distance_y * swipe_state

            case 'center2left_side':
                scale_range = self.side_scale_factor / self.center_scale_factor
                scale_factor = 1 - scale_range * swipe_state
                alpha_range = 255 - self.side_alpha
                alpha = 255 - alpha_range * swipe_state
                distance_x = abs(self.center_topleft[0] - self.left_topleft[0])
                distance_y = abs(self.center_topleft[1] - self.left_topleft[1])
                new_x = self.center_topleft[0] - distance_x * swipe_state
                new_y = self.center_topleft[1] + distance_y * swipe_state
            case 'center2right_side':
                scale_range = self.side_scale_factor / self.center_scale_factor
                scale_factor = 1 - scale_range * swipe_state
                alpha_range = 255 - self.side_alpha
                alpha = 255 - alpha_range * swipe_state
                distance_x = abs(self.right_topleft[0] - self.center_topleft[0])
                distance_y = abs(self.right_topleft[1] - self.center_topleft[1])
                new_x = self.center_topleft[0] + distance_x * swipe_state
                new_y = self.center_topleft[1] + distance_y * swipe_state

            case 'side2nowhere':
                scale_factor = 1
                alpha = self.side_alpha * (1 - swipe_state)
                new_x, new_y = image.rect.topleft

            case 'nowhere2side':
                scale_factor = 1
                alpha = self.side_alpha * swipe_state
                new_x, new_y = image.rect.topleft
            case _:
                raise Exception("Invalid mode")

        image = image.resize(scale_factor)
        image.set_alpha(alpha)
        image.set_position((new_x, new_y))

        return image

    def activate_swipe(self, mode: str):
        self.swiping = True
        if mode == 'previous':
            self.swipe_mode = 'previous'
            # swipe new image to the left one
            new_left = self.side_carousel_previous[self.left.hashed]
            new_left.set_position(self.left_topleft)
            new_center = self.left
            new_right = self.center
            gone_right = self.right
            self.swiping_images = [new_left, new_center, new_right, gone_right]
        elif mode == 'next':
            self.swipe_mode = 'next'
            # swipe new image to the right one
            new_left = self.center
            new_center = self.right
            new_right = self.side_carousel_next[self.right.hashed]
            new_right.set_position(self.right_topleft)
            gone_left = self.left
            self.swiping_images = [new_left, new_center, new_right, gone_left]

    def increase_swipe(self):
        # refresh the background
        self.clean_background()
        if self.swipe_state == self.max_swipe_state:
            self.swiping = False
            self.swipe_state = 0
            if self.swipe_mode == 'next':
                self.next()
            elif self.swipe_mode == 'previous':
                self.previous()
            return

        self.swipe_state += 1

        if self.swipe_mode == "previous":
            # swipe the new images to the left
            new_left = self.swipe_image(self.swiping_images[0], 'nowhere2side')
            new_center = self.swipe_image(self.swiping_images[1], 'left_side2center')
            new_right = self.swipe_image(self.swiping_images[2], 'center2right_side')
            gone_right = self.swipe_image(self.swiping_images[3], 'side2nowhere')

            # blit the new images
            self.blit(new_left, new_left.rect.topleft)
            self.blit(new_center, new_center.rect.topleft)
            self.blit(new_right, new_right.rect.topleft)
            self.blit(gone_right, gone_right.rect.topleft)

        elif self.swipe_mode == "next":
            # swipe the new images to the right
            new_left = self.swipe_image(self.swiping_images[0], 'center2left_side')
            new_center = self.swipe_image(self.swiping_images[1], 'right_side2center')
            new_right = self.swipe_image(self.swiping_images[2], 'nowhere2side')
            gone_left = self.swipe_image(self.swiping_images[3], 'side2nowhere')

            # blit the new images
            self.blit(new_left, new_left.rect.topleft)
            self.blit(new_center, new_center.rect.topleft)
            self.blit(new_right, new_right.rect.topleft)
            self.blit(gone_left, gone_left.rect.topleft)


class Number(pygame.Surface):
    def __init__(self, number: int, img=None):
        self.number = number

        if img is not None:
            super().__init__(img.get_size(), pygame.SRCALPHA, 32)
            self.blit(img, (0, 0))
            self.rect = self.get_rect()

        else:
            images = []
            for x in str(number):
                image = pygame.image.load(f"assets/numbers/{x}.png").convert_alpha()
                images.append(image)

            total_width = sum([image.get_width() for image in images])
            total_height = images[0].get_height()

            super().__init__((total_width, total_height), pygame.SRCALPHA, 32)
            self.rect = self.get_rect()

            w = 0
            for image in images:
                self.blit(image, (w, 0))
                w += image.get_width()

    def resize(self, scale_factor: float | int):
        w, h = self.get_size()
        new_w, new_h = w * scale_factor, h * scale_factor
        img = pygame.transform.scale(self, [new_w, new_h])
        return Number(self.number, img)

    def set_position(self, position: tuple[float, float]):
        self.rect.topleft = position
