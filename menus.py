import pygame
from widgets import Image, Button
from pygame.locals import *


class MenuBackground(pygame.Surface):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        self.buttons = []

        # load images for the background
        self.sea_image = Image(self, "sea.png")
        self.captain_flip_image = Image(self, "captain_flip_logo.png", convert_alpha=True)

        # resize background image
        scale_factor = size[0] / self.sea_image.rect.w
        self.sea_image = self.sea_image.resize(scale_factor)

        # resize logo
        scale_factor = (size[0] // 3) / self.captain_flip_image.rect.w
        self.captain_flip_image = self.captain_flip_image.resize(scale_factor)

        # set positions of the logo and background
        self.captain_flip_image.set_position((size[0]//2 - self.captain_flip_image.rect.w/2, -size[1]//20))
        self.sea_image.set_position((0, 0))

        # copy the images on the surface
        self.blit(self.sea_image, self.sea_image.rect.topleft)
        self.blit(self.captain_flip_image, self.captain_flip_image.rect.topleft)

        # load parchment image
        self.parchment_image = Image(self, "parchment.png", convert_alpha=True)

        # resize parchment
        scale_factor = (size[0] // 3) / self.parchment_image.rect.w
        self.parchment_image = self.parchment_image.resize(scale_factor)

        # set positions of the parchment
        self.parchment_image.set_position((size[0]//2 - self.parchment_image.rect.w//2,
                                           size[1]//1.5 - self.parchment_image.rect.h//2))

        # copy the images on the surface
        self.blit(self.parchment_image, self.parchment_image.rect.topleft)


class HomeMenu(MenuBackground):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        # load images for buttons
        self.login_button = Button(self, "login.png", call=lambda: print("hi"), convert_alpha=True)

        # resize login button
        scale_factor = (self.parchment_image.rect.w // 3) / self.login_button.rect.w
        self.login_button = self.login_button.resize(scale_factor)

        # set positions of the login button
        self.login_button.set_position((self.parchment_image.rect.w//2 - self.login_button.rect.w // 2 + self.parchment_image.rect.x,
                                       self.parchment_image.rect.h//4 + self.parchment_image.rect.y))

        # copy the images on the surface
        self.blit(self.login_button, self.login_button.rect.topleft)

        self.buttons.append(self.login_button)

    def event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # coordinates of click point.
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.call()
