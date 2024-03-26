import pygame.event

from widgets import Image, Button, InputBox, Carousel, Number
from pygame.locals import *
from database import Database
from parameters import *


class MenuBackground(pygame.Surface):
    """
    This class is used to create a background for the menu
    """

    def __init__(self, size: tuple[float, float], with_parchment=True, pre_menu_event=None, with_logo=True):
        super().__init__(size)
        self.with_parchment = with_parchment
        self.with_logo = with_logo

        self.buttons = []
        self.hover_dict = {}

        # load images for the background
        self.sea_image = Image("assets/sea.png")
        self.captain_flip_image = Image("assets/captain_flip_logo.png", convert_alpha=True)

        # resize background image
        scale_factor = size[0] / self.sea_image.rect.w
        self.sea_image = self.sea_image.resize(scale_factor)

        # resize logo
        scale_factor = (size[0] // 3) / self.captain_flip_image.rect.w
        self.captain_flip_image = self.captain_flip_image.resize(scale_factor)

        # set positions of the logo and background
        self.captain_flip_image.set_position((size[0] // 2 - self.captain_flip_image.rect.w / 2, -size[1] // 20))
        self.sea_image.set_position((0, 0))

        # copy the images on the surface
        self.blit(self.sea_image, self.sea_image.rect.topleft)
        if with_logo:
            self.blit(self.captain_flip_image, self.captain_flip_image.rect.topleft)

        if with_parchment:
            # load parchment image
            self.parchment_image = Image("assets/parchment.png", convert_alpha=True)

            # resize parchment
            scale_factor = (size[0] // 3) / self.parchment_image.rect.w
            self.parchment_image = self.parchment_image.resize(scale_factor)

            # set positions of the parchment
            self.parchment_image.set_position((size[0] // 2 - self.parchment_image.rect.w // 2,
                                               size[1] // 1.5 - self.parchment_image.rect.h // 2))

            # copy the image on the surface
            self.blit(self.parchment_image, self.parchment_image.rect.topleft)

        # add close button
        self.close_button = Button("assets/buttons/x.png", call=lambda: (pygame.quit(), exit(0)),
                                   convert_alpha=True)
        self.close_button_hover = Image("assets/buttons/x_hover.png", convert_alpha=True)
        scale_factor = (size[0] // 20) / self.close_button.rect.w
        self.close_button = self.close_button.resize(scale_factor)
        self.close_button_hover = self.close_button_hover.resize(scale_factor)
        self.close_button.set_position((size[0] - self.close_button.rect.w * 1.5, self.close_button.rect.h // 2))
        self.close_button_hover.set_position((size[0] - self.close_button.rect.w * 1.5, self.close_button.rect.h // 2))

        self.buttons.append(self.close_button)
        self.hover_dict[self.close_button.hashed] = self.close_button_hover
        self.blit(self.close_button, self.close_button.rect.topleft)

        if pre_menu_event is not None:
            self.backward_button = Button("assets/buttons/left_arrow.png", call=lambda: pygame.event.post(
                pygame.event.Event(pre_menu_event)), convert_alpha=True)
            self.backward_button_hover = Image("assets/buttons/left_arrow_hover.png", convert_alpha=True)
            scale_factor = (size[0] // 10) / self.backward_button.rect.w
            self.backward_button = self.backward_button.resize(scale_factor)
            self.backward_button_hover = self.backward_button_hover.resize(scale_factor)
            self.backward_button.set_position((self.backward_button.rect.w // 2, self.backward_button.rect.h // 2))
            self.backward_button_hover.set_position((self.backward_button.rect.w // 2,
                                                     self.backward_button.rect.h // 2))

            self.buttons.append(self.backward_button)
            self.hover_dict[self.backward_button.hashed] = self.backward_button_hover
            self.blit(self.backward_button, self.backward_button.rect.topleft)

    def blit_background(self):
        self.blit(self.sea_image, self.sea_image.rect.topleft)
        if self.with_logo:
            self.blit(self.captain_flip_image, self.captain_flip_image.rect.topleft)
        if self.with_parchment:
            self.blit(self.parchment_image, self.parchment_image.rect.topleft)
        self.blit(self.close_button, self.close_button.rect.topleft)
        self.blit(self.backward_button, self.backward_button.rect.topleft)

    def button_event_handler(self, event):
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


class FirstMenu(MenuBackground):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        # load images for buttons
        self.login_button = Button("assets/buttons/login.png",
                                   call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_LOGIN)),
                                   convert_alpha=True)
        self.register_button = Button("assets/buttons/register.png",
                                      call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_REGISTER)),
                                      convert_alpha=True)
        self.quit_button = Button("assets/buttons/quit.png", call=lambda: (pygame.quit(), exit(0)),
                                  convert_alpha=True)

        # load images for the hover effect
        self.login_button_hover = Image("assets/buttons/login_hover.png", convert_alpha=True)
        self.register_button_hover = Image("assets/buttons/register_hover.png", convert_alpha=True)
        self.quit_button_hover = Image("assets/buttons/quit_hover.png", convert_alpha=True)

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
        login_button_pos = (
            self.parchment_image.rect.w // 2 - self.login_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 5.5 + self.parchment_image.rect.y)
        register_button_pos = (
            self.parchment_image.rect.w // 2 - self.register_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 2.35 + self.parchment_image.rect.y)
        quit_button_pos = (
            self.parchment_image.rect.w // 2 - self.quit_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 1.5 + self.parchment_image.rect.y)

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

    def event_handler(self, event):
        self.button_event_handler(event)


class HomeMenu(MenuBackground):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size, pre_menu_event=CHANGE_TO_FIRST)

        # load images for buttons (gamemode, stats, quit)
        self.gamemode_button = Button("assets/buttons/gamemode.png",
                                      call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_GAMEMODE)),
                                      convert_alpha=True)
        self.stats_button = Button("assets/buttons/stats.png",
                                   call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_STATS)),
                                   convert_alpha=True)
        self.quit_button = Button("assets/buttons/quit.png", call=lambda: (pygame.quit(), exit(0)),
                                  convert_alpha=True)

        # load images for the hover effect
        self.gamemode_button_hover = Image("assets/buttons/gamemode_hover.png", convert_alpha=True)
        self.stats_button_hover = Image("assets/buttons/stats_hover.png", convert_alpha=True)
        self.quit_button_hover = Image("assets/buttons/quit_hover.png", convert_alpha=True)

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
        gamemode_button_pos = (
            self.parchment_image.rect.w // 2 - self.gamemode_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 5.5 + self.parchment_image.rect.y)
        stats_button_pos = (
            self.parchment_image.rect.w // 2 - self.stats_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 2.35 + self.parchment_image.rect.y)
        quit_button_pos = (
            self.parchment_image.rect.w // 2 - self.quit_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 1.5 + self.parchment_image.rect.y)

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

    def event_handler(self, event):
        self.button_event_handler(event)


class LoginMenu(MenuBackground):
    def __init__(self, size, mode, player=None):
        super().__init__(size, pre_menu_event=CHANGE_TO_FIRST)

        self.db = Database("database.csv")
        self.mode = mode
        self.player = player

        # rotate parchment
        self.parchment_image = self.parchment_image.rotate(90)

        # resize parchment
        scale_factor = size[0] // 2.5 / self.parchment_image.rect.w
        self.parchment_image = self.parchment_image.resize(scale_factor)

        # change parchment position
        parchment_pos = (
            size[0] // 2 - self.parchment_image.rect.w // 2, size[1] // 2 - self.parchment_image.rect.h // 3)
        self.parchment_image.set_position(parchment_pos)

        # refresh background to cover old parchment and blit it above
        self.blit_background()

        if mode == "login":
            # place login button
            self.login_button = Button("assets/buttons/login.png", call=lambda: self.login(),
                                       convert_alpha=True)
            self.login_button_hover = Image("assets/buttons/login_hover.png", convert_alpha=True)
            scale_factor = (self.parchment_image.rect.w // 7.5) / 130
            self.login_button = self.login_button.resize(scale_factor)
            self.login_button_hover = self.login_button_hover.resize(scale_factor)
            self.hover_dict[self.login_button.hashed] = self.login_button_hover
            login_button_pos = (
                self.parchment_image.rect.w // 2 - self.login_button.rect.w // 2 + self.parchment_image.rect.x,
                self.parchment_image.rect.h // 1.70 + self.parchment_image.rect.y)
            self.login_button.set_position(login_button_pos)
            self.login_button_hover.set_position(login_button_pos)
            self.buttons.append(self.login_button)
            self.blit(self.login_button, self.login_button.rect.topleft)
        else:
            # place register button
            self.register_button = Button("assets/buttons/register.png", call=lambda: self.register(),
                                          convert_alpha=True)
            self.register_button_hover = Image("assets/buttons/register_hover.png", convert_alpha=True)
            scale_factor = (self.parchment_image.rect.w // 7.5) / 130
            self.register_button = self.register_button.resize(scale_factor)
            self.register_button_hover = self.register_button_hover.resize(scale_factor)
            self.hover_dict[self.register_button.hashed] = self.register_button_hover
            register_button_pos = (
                self.parchment_image.rect.w // 2 - self.register_button.rect.w // 2 + self.parchment_image.rect.x,
                self.parchment_image.rect.h // 1.70 + self.parchment_image.rect.y)
            self.register_button.set_position(register_button_pos)
            self.register_button_hover.set_position(register_button_pos)
            self.buttons.append(self.register_button)

            self.blit(self.register_button, self.register_button.rect.topleft)

        # initialize boxes
        boxes_w, boxes_h = self.parchment_image.rect.w // 1.75, 50
        box1_pos = (self.parchment_image.rect.x + self.parchment_image.rect.w // 2 - boxes_w // 2,
                    self.parchment_image.rect.y + self.parchment_image.rect.h // 2.75 - boxes_h // 2)
        box2_pos = (self.parchment_image.rect.x + self.parchment_image.rect.w // 2 - boxes_w // 2,
                    self.parchment_image.rect.y + self.parchment_image.rect.h // 2 - boxes_h // 2)
        self.input_box_username = InputBox(box1_pos[0], box1_pos[1], boxes_w, boxes_h, under_text="Username")
        self.input_box_password = InputBox(box2_pos[0], box2_pos[1], boxes_w, boxes_h, under_text="Password")
        self.input_boxes = [self.input_box_username, self.input_box_password]

    def login(self):
        username = self.input_box_username.text
        password = self.input_box_password.text

        result = self.db.sign_in(username, password)
        if result:
            self.player.stats = (self.db.victories, self.db.defeats, self.db.draws)
            pygame.event.post(pygame.event.Event(UPDATE_STATS))
            pygame.event.post(pygame.event.Event(CHANGE_TO_HOME))
        else:
            print("wrong username or password")

    def register(self):
        username = self.input_box_username.text
        password = self.input_box_password.text

        self.db.sign_up(username, password)

        pygame.event.post(pygame.event.Event(RESET_PLAYER))
        pygame.event.post(pygame.event.Event(CHANGE_TO_GAMEMODE))

    def event_handler(self, event):
        self.button_event_handler(event)

        for box in self.input_boxes:
            box.handle_event(event)

        # refresh parchment then draw input boxes above and login button
        self.blit(self.parchment_image, self.parchment_image.rect.topleft)
        for box in self.input_boxes:
            box.draw(self)

        if self.mode == "login":
            if self.login_button.hover:
                self.blit(self.login_button_hover, self.login_button.rect.topleft)
            else:
                self.blit(self.login_button, self.login_button.rect.topleft)
        else:
            if self.register_button.hover:
                self.blit(self.register_button_hover, self.register_button.rect.topleft)
            else:
                self.blit(self.register_button, self.register_button.rect.topleft)


class GameModeMenu(MenuBackground):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size, pre_menu_event=CHANGE_TO_HOME)

        # load images for buttons (gamemode, stats, quit)
        self.single_player_button = Button("assets/buttons/single_player.png",
                                           call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_CHOOSE_BOARD)),
                                           convert_alpha=True)
        self.multiplayer_button = Button("assets/buttons/multiplayer.png",
                                         call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_CHOOSE_BOARD)),
                                         convert_alpha=True)
        self.rules_button = Button("assets/buttons/rules.png",
                                   call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_RULES)),
                                   convert_alpha=True)

        # load images for the hover effect
        self.single_player_button_hover = Image("assets/buttons/single_player_hover.png", convert_alpha=True)
        self.multiplayer_button_hover = Image("assets/buttons/multiplayer_hover.png", convert_alpha=True)
        self.rules_button_hover = Image("assets/buttons/rules_hover.png", convert_alpha=True)

        # resize buttons
        scale_factor = (self.parchment_image.rect.w // 4.5) / 140
        self.single_player_button = self.single_player_button.resize(scale_factor)
        self.multiplayer_button = self.multiplayer_button.resize(scale_factor)
        self.stats_button = self.rules_button.resize(scale_factor)

        # resize hover effect
        self.single_player_button_hover = self.single_player_button_hover.resize(scale_factor)
        self.multiplayer_button_hover = self.multiplayer_button_hover.resize(scale_factor)
        self.stats_button_hover = self.rules_button_hover.resize(scale_factor)

        # add hover effect to the hover_dict
        self.hover_dict[self.single_player_button.hashed] = self.single_player_button_hover
        self.hover_dict[self.multiplayer_button.hashed] = self.multiplayer_button_hover
        self.hover_dict[self.stats_button.hashed] = self.stats_button_hover

        # set positions of the buttons
        single_player_button_pos = (
            self.parchment_image.rect.w // 2 - self.single_player_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 5.5 + self.parchment_image.rect.y)
        multiplayer_button_pos = (
            self.parchment_image.rect.w // 2 - self.multiplayer_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 2.35 + self.parchment_image.rect.y)
        quit_button_pos = (
            self.parchment_image.rect.w // 2 - self.stats_button.rect.w // 2 + self.parchment_image.rect.x,
            self.parchment_image.rect.h // 1.5 + self.parchment_image.rect.y)

        self.single_player_button.set_position(single_player_button_pos)
        self.multiplayer_button.set_position(multiplayer_button_pos)
        self.stats_button.set_position(quit_button_pos)

        # set positions of the hover effect
        self.single_player_button_hover.set_position(single_player_button_pos)
        self.multiplayer_button_hover.set_position(multiplayer_button_pos)
        self.stats_button_hover.set_position(quit_button_pos)

        # copy the images on the surface
        self.blit(self.single_player_button, self.single_player_button.rect.topleft)
        self.blit(self.multiplayer_button, self.multiplayer_button.rect.topleft)
        self.blit(self.stats_button, self.stats_button.rect.topleft)

        self.buttons.extend([self.single_player_button, self.multiplayer_button, self.stats_button])

    def event_handler(self, event):
        self.button_event_handler(event)


class ChooseBoardMenu(MenuBackground):
    def __init__(self, size):
        super().__init__(size, pre_menu_event=CHANGE_TO_GAMEMODE, with_parchment=False)

        self.carousel = Carousel(size, size, [f"assets/boards/board_{i}.png" for i in range(1, 6)], self.sea_image)

        self.blit(self.carousel, (0, 0))

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.carousel.left.rect.collidepoint(pos):
                self.carousel.previous()
                self.blit(self.carousel, (0, 0))
            elif self.carousel.right.rect.collidepoint(pos):
                self.carousel.next()
                self.blit(self.carousel, (0, 0))
            elif self.carousel.center.rect.collidepoint(pos):
                print("start game")

        self.button_event_handler(event)


class RulesMenu(MenuBackground):
    def __init__(self, size):
        super().__init__(size, pre_menu_event=CHANGE_TO_GAMEMODE, with_parchment=False, with_logo=False)
        self.current_image = 0
        self.images = []

        # load rules image
        self.rules_image1 = Image("assets/rules/rules_1.png")
        self.rules_image2 = Image("assets/rules/rules_2.png")
        self.rules_image3 = Image("assets/rules/rules_3.png")

        # resize rules image
        scale_factor = (size[0] // 2.25) / self.rules_image1.rect.w
        self.rules_image1 = self.rules_image1.resize(scale_factor)
        self.rules_image2 = self.rules_image2.resize(scale_factor)
        self.rules_image3 = self.rules_image3.resize(scale_factor)

        # set positions of the rules image
        rules_pos = (size[0] // 2 - self.rules_image1.rect.w // 2, size[1] // 2 - self.rules_image1.rect.h // 2)
        self.rules_image1.set_position(rules_pos)
        self.rules_image2.set_position(rules_pos)
        self.rules_image3.set_position(rules_pos)

        # add images to the list
        self.images.extend([self.rules_image1, self.rules_image2, self.rules_image3])

        # load right and left buttons
        self.left_button = Button("assets/buttons/left.png", call=lambda: self.previous(),
                                  convert_alpha=True)
        self.right_button = Button("assets/buttons/right.png", call=lambda: self.next(),
                                   convert_alpha=True)

        # load hover images
        self.left_button_hover = Image("assets/buttons/left_hover.png", convert_alpha=True)
        self.right_button_hover = Image("assets/buttons/right_hover.png", convert_alpha=True)

        # resize buttons and hover images
        scale_factor = (size[0] // 10) / 100
        self.left_button = self.left_button.resize(scale_factor)
        self.right_button = self.right_button.resize(scale_factor)
        self.left_button_hover = self.left_button_hover.resize(scale_factor)
        self.right_button_hover = self.right_button_hover.resize(scale_factor)

        # set positions of the buttons and hover images
        left_button_pos = (rules_pos[0] - self.left_button.rect.w - 40,
                           rules_pos[1] + self.rules_image1.rect.h // 2 - self.left_button.rect.h // 2)
        right_button_pos = (rules_pos[0] + self.rules_image1.rect.w + 40,
                            rules_pos[1] + self.rules_image1.rect.h // 2 - self.right_button.rect.h // 2)

        self.left_button.set_position(left_button_pos)
        self.right_button.set_position(right_button_pos)
        self.left_button_hover.set_position(left_button_pos)
        self.right_button_hover.set_position(right_button_pos)

        # load rules position image
        self.rules_1_3 = Image("assets/rules/1_3.png", convert_alpha=True)
        self.rules_2_3 = Image("assets/rules/2_3.png", convert_alpha=True)
        self.rules_3_3 = Image("assets/rules/3_3.png", convert_alpha=True)

        # resize rules position image
        scale_factor = (size[0] // 20) / self.rules_1_3.rect.w
        self.rules_1_3 = self.rules_1_3.resize(scale_factor)
        self.rules_2_3 = self.rules_2_3.resize(scale_factor)
        self.rules_3_3 = self.rules_3_3.resize(scale_factor)

        # set positions of the rules position image
        rules_pos = (size[0] // 2 - self.rules_1_3.rect.w // 2,
                     self.rules_image1.rect.y + self.rules_image1.rect.h + self.rules_1_3.rect.h // 2)
        self.rules_1_3.set_position(rules_pos)
        self.rules_2_3.set_position(rules_pos)
        self.rules_3_3.set_position(rules_pos)
        self.rules_position_images = [self.rules_1_3, self.rules_2_3, self.rules_3_3]

        # copy the images on the surface
        self.blit(self.rules_image1, self.rules_image1.rect.topleft)
        self.blit(self.left_button, self.left_button.rect.topleft)
        self.blit(self.right_button, self.right_button.rect.topleft)
        self.blit(self.rules_1_3, self.rules_1_3.rect.topleft)

    def next(self):
        self.current_image = self.current_image + 1 if self.current_image < 2 else 0
        self.blit(self.images[self.current_image], self.images[self.current_image].rect.topleft)
        self.blit(self.sea_image, self.rules_position_images[self.current_image].rect.topleft,
                  self.rules_position_images[self.current_image].rect)
        self.blit(self.rules_position_images[self.current_image],
                  self.rules_position_images[self.current_image].rect.topleft)

    def previous(self):
        self.current_image = self.current_image - 1 if self.current_image > 0 else 2
        self.blit(self.images[self.current_image], self.images[self.current_image].rect.topleft)
        self.blit(self.sea_image, self.rules_position_images[self.current_image].rect.topleft,
                  self.rules_position_images[self.current_image].rect)
        self.blit(self.rules_position_images[self.current_image],
                  self.rules_position_images[self.current_image].rect.topleft)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.left_button.rect.collidepoint(pos):
                self.previous()
            elif self.right_button.rect.collidepoint(pos):
                self.next()
        elif event.type == MOUSEMOTION:
            mouse_pos = event.pos
            if self.left_button.rect.collidepoint(mouse_pos):
                if not self.left_button.hover:
                    self.left_button.hover = True
                    self.blit(self.left_button_hover, self.left_button.rect.topleft)
            else:
                if self.left_button.hover:
                    self.left_button.hover = False
                    self.blit(self.left_button, self.left_button.rect.topleft)

            if self.right_button.rect.collidepoint(mouse_pos):
                if not self.right_button.hover:
                    self.right_button.hover = True
                    self.blit(self.right_button_hover, self.right_button.rect.topleft)
            else:
                if self.right_button.hover:
                    self.right_button.hover = False
                    self.blit(self.right_button, self.right_button.rect.topleft)

        self.button_event_handler(event)


class StatsMenu(MenuBackground):
    def __init__(self, size):
        super().__init__(size, pre_menu_event=CHANGE_TO_HOME)

        # rotate parchment
        self.parchment_image = self.parchment_image.rotate(90)

        # resize parchment
        scale_factor = size[0] // 2.5 / self.parchment_image.rect.w
        self.parchment_image = self.parchment_image.resize(scale_factor)

        # change parchment position
        parchment_pos = (
            size[0] // 2 - self.parchment_image.rect.w // 2, size[1] // 2 - self.parchment_image.rect.h // 3)
        self.parchment_image.set_position(parchment_pos)

        # refresh background to cover old parchment and blit it above
        self.blit_background()

        # load stats image
        self.wins_image = Image("assets/stats/wins.png", convert_alpha=True)
        self.losses_image = Image("assets/stats/losses.png", convert_alpha=True)
        self.draws_image = Image("assets/stats/draws.png", convert_alpha=True)

        # resize stats image
        scale_factor = (size[0] // 12.5) / self.wins_image.rect.w
        self.wins_image = self.wins_image.resize(scale_factor)
        self.losses_image = self.losses_image.resize(scale_factor)
        self.draws_image = self.draws_image.resize(scale_factor)

        # set positions of the stats image
        stats_pos = (self.parchment_image.rect.x + self.parchment_image.rect.w // 5, self.parchment_image.rect.y + self.parchment_image.rect.h // 3.5)
        self.wins_image.set_position(stats_pos)
        self.losses_image.set_position((stats_pos[0], stats_pos[1] + self.parchment_image.rect.h // 5.5))
        self.draws_image.set_position((stats_pos[0], stats_pos[1] + self.parchment_image.rect.h // 2.75))

        # blit stats image
        self.blit(self.wins_image, self.wins_image.rect.topleft)
        self.blit(self.losses_image, self.losses_image.rect.topleft)
        self.blit(self.draws_image, self.draws_image.rect.topleft)

        # load number images
        self.wins_number = Number(0)
        self.losses_number = Number(0)
        self.draws_number = Number(0)

        # resize number images
        self.number_scale_factor = (size[0] // 35) / self.wins_number.rect.w
        self.wins_number = self.wins_number.resize(self.number_scale_factor)
        self.losses_number = self.losses_number.resize(self.number_scale_factor)
        self.draws_number = self.draws_number.resize(self.number_scale_factor)

        # set positions of the number images
        number_pos = (self.parchment_image.rect.x + self.parchment_image.rect.w - self.parchment_image.rect.w // 2.5, self.parchment_image.rect.y + self.parchment_image.rect.h // 3.5)
        self.wins_number.set_position(number_pos)
        self.losses_number.set_position((number_pos[0], number_pos[1] + self.parchment_image.rect.h // 5.5))
        self.draws_number.set_position((number_pos[0], number_pos[1] + self.parchment_image.rect.h // 2.75))

        # blit number images
        self.blit(self.wins_number, self.wins_number.rect.topleft)
        self.blit(self.losses_number, self.losses_number.rect.topleft)
        self.blit(self.draws_number, self.draws_number.rect.topleft)
        
        self.update_stats((2, 4, 18))

    def update_stats(self, new_stats: tuple[int, int, int]):
        self.wins_number = Number(new_stats[0])
        self.losses_number = Number(new_stats[1])
        self.draws_number = Number(new_stats[2])

        # resize number images
        self.wins_number = self.wins_number.resize(self.number_scale_factor)
        self.losses_number = self.losses_number.resize(self.number_scale_factor)
        self.draws_number = self.draws_number.resize(self.number_scale_factor)

        # set positions of the number images
        number_pos = (self.parchment_image.rect.x + self.parchment_image.rect.w - self.parchment_image.rect.w // 2.5, self.parchment_image.rect.y + self.parchment_image.rect.h // 3.5)
        self.wins_number.set_position(number_pos)
        self.losses_number.set_position((number_pos[0], number_pos[1] + self.parchment_image.rect.h // 5.5))
        self.draws_number.set_position((number_pos[0], number_pos[1] + self.parchment_image.rect.h // 2.75))
        
        # blit number images
        self.blit_background()
        self.blit(self.wins_image, self.wins_image.rect.topleft)
        self.blit(self.losses_image, self.losses_image.rect.topleft)
        self.blit(self.draws_image, self.draws_image.rect.topleft)
        self.blit(self.wins_number, self.wins_number.rect.topleft)
        self.blit(self.losses_number, self.losses_number.rect.topleft)
        self.blit(self.draws_number, self.draws_number.rect.topleft)
        
    def event_handler(self, event):
        self.button_event_handler(event)

    def event_handler(self, event):
        self.button_event_handler(event)
