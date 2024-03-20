import pygame
from widgets import Image, Button
from pygame.locals import *


class MenuBackground(pygame.Surface):
    """
    This class is used to create a background for the menu
    """
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        self.buttons = []
        self.hover_dict = {}

        # load images for the background
        self.sea_image = Image(self, "assets/sea.png")
        self.captain_flip_image = Image(self, "assets/captain_flip_logo.png", convert_alpha=True)

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
        self.parchment_image = Image(self, "assets/parchment.png", convert_alpha=True)

        # resize parchment
        scale_factor = (size[0] // 3) / self.parchment_image.rect.w
        self.parchment_image = self.parchment_image.resize(scale_factor)

        # set positions of the parchment
        self.parchment_image.set_position((size[0]//2 - self.parchment_image.rect.w//2,
                                           size[1]//1.5 - self.parchment_image.rect.h//2))

        # copy the image on the surface
        self.blit(self.parchment_image, self.parchment_image.rect.topleft)

    def event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # coordinates of click point.
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.call()
        elif event.type == MOUSEMOTION:
            mouse_pos = event.pos
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if not button.hover:
                        button.hover = True
                        self.blit(self.hover_dict[button.hashed], button.rect.topleft)
                else:
                    if button.hover:
                        button.hover = False
                        self.blit(button, button.rect.topleft)


class LoginMenu(MenuBackground):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        # load images for buttons
        self.login_button = Button(self, "assets/login.png", call=lambda: print("login"), convert_alpha=True)
        self.register_button = Button(self, "assets/register.png", call=lambda: print("register"), convert_alpha=True)
        self.quit_button = Button(self, "assets/quit.png", call=lambda: (pygame.quit(), exit(0)), convert_alpha=True)

        # load images for the hover effect
        self.login_button_hover = Image(self, "assets/login_hover.png", convert_alpha=True)
        self.register_button_hover = Image(self, "assets/register_hover.png", convert_alpha=True)
        self.quit_button_hover = Image(self, "assets/quit_hover.png", convert_alpha=True)

        # resize buttons
        scale_factor = (self.parchment_image.rect.w // 4.5) / 130
        self.login_button = self.login_button.resize(scale_factor)
        self.register_button = self.register_button.resize(scale_factor)
        self.quit_button = self.quit_button.resize(scale_factor)

        # resize hover effect
        self.login_button_hover = self.login_button_hover.resize(scale_factor)
        self.register_button_hover = self.register_button_hover.resize(scale_factor)
        self.quit_button_hover = self.quit_button_hover.resize(scale_factor)

        # add hover effect to the hover_dict
        self.hover_dict[self.login_button.hashed] = self.login_button_hover
        self.hover_dict[self.register_button.hashed] = self.register_button_hover
        self.hover_dict[self.quit_button.hashed] = self.quit_button_hover

        # set positions of the buttons
        login_button_pos = (self.parchment_image.rect.w//2 - self.login_button.rect.w // 2 + self.parchment_image.rect.x,
                            self.parchment_image.rect.h//5.5 + self.parchment_image.rect.y)
        register_button_pos = (self.parchment_image.rect.w//2 - self.register_button.rect.w // 2 + self.parchment_image.rect.x,
                               self.parchment_image.rect.h//2.35 + self.parchment_image.rect.y)
        quit_button_pos = (self.parchment_image.rect.w//2 - self.quit_button.rect.w // 2 + self.parchment_image.rect.x,
                           self.parchment_image.rect.h//1.5 + self.parchment_image.rect.y)

        self.login_button.set_position(login_button_pos)
        self.register_button.set_position(register_button_pos)
        self.quit_button.set_position(quit_button_pos)

        # set positions of the hover effect
        self.login_button_hover.set_position(login_button_pos)
        self.register_button_hover.set_position(register_button_pos)
        self.quit_button_hover.set_position(quit_button_pos)

        # copy the images on the surface
        self.blit(self.login_button, self.login_button.rect.topleft)
        self.blit(self.register_button, self.register_button.rect.topleft)
        self.blit(self.quit_button, self.quit_button.rect.topleft)

        self.buttons.extend([self.login_button, self.register_button, self.quit_button])


class HomeMenu(MenuBackground):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        self.hover_dict = {}

        # load images for buttons (gamemode, stats, quit)
        self.gamemode_button = Button(self, "assets/gamemode.png", call=lambda: print("gamemode"), convert_alpha=True)
        self.stats_button = Button(self, "assets/stats.png", call=lambda: print("stats"), convert_alpha=True)
        self.quit_button = Button(self, "assets/quit.png", call=lambda: (pygame.quit(), exit(0)), convert_alpha=True)

        # load images for the hover effect
        self.gamemode_button_hover = Image(self, "assets/gamemode_hover.png", convert_alpha=True)
        self.stats_button_hover = Image(self, "assets/stats_hover.png", convert_alpha=True)
        self.quit_button_hover = Image(self, "assets/quit_hover.png", convert_alpha=True)

        # resize buttons
        scale_factor = (self.parchment_image.rect.w // 4.5) / 130
        self.gamemode_button = self.gamemode_button.resize(scale_factor)
        self.stats_button = self.stats_button.resize(scale_factor)
        self.quit_button = self.quit_button.resize(scale_factor)

        # resize hover effect
        self.gamemode_button_hover = self.gamemode_button_hover.resize(scale_factor)
        self.stats_button_hover = self.stats_button_hover.resize(scale_factor)
        self.quit_button_hover = self.quit_button_hover.resize(scale_factor)

        # add hover effect to the hover_dict
        self.hover_dict[self.gamemode_button.hashed] = self.gamemode_button_hover
        self.hover_dict[self.stats_button.hashed] = self.stats_button_hover
        self.hover_dict[self.quit_button.hashed] = self.quit_button_hover

        # set positions of the buttons
        gamemode_button_pos = (self.parchment_image.rect.w//2 - self.gamemode_button.rect.w // 2 + self.parchment_image.rect.x,
                            self.parchment_image.rect.h//5.5 + self.parchment_image.rect.y)
        stats_button_pos = (self.parchment_image.rect.w//2 - self.stats_button.rect.w // 2 + self.parchment_image.rect.x,
                               self.parchment_image.rect.h//2.35 + self.parchment_image.rect.y)
        quit_button_pos = (self.parchment_image.rect.w//2 - self.quit_button.rect.w // 2 + self.parchment_image.rect.x,
                           self.parchment_image.rect.h//1.5 + self.parchment_image.rect.y)

        self.gamemode_button.set_position(gamemode_button_pos)
        self.stats_button.set_position(stats_button_pos)
        self.quit_button.set_position(quit_button_pos)

        # set positions of the hover effect
        self.gamemode_button_hover.set_position(gamemode_button_pos)
        self.stats_button_hover.set_position(stats_button_pos)
        self.quit_button_hover.set_position(quit_button_pos)

        # copy the images on the surface
        self.blit(self.gamemode_button, self.gamemode_button.rect.topleft)
        self.blit(self.stats_button, self.stats_button.rect.topleft)
        self.blit(self.quit_button, self.quit_button.rect.topleft)

        self.buttons.extend([self.gamemode_button, self.stats_button, self.quit_button])
