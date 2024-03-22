from widgets import Image, Button, InputBox
from pygame.locals import *
from database import Database
from parameters import *


class MenuBackground(pygame.Surface):
    """
    This class is used to create a background for the menu
    """

    def __init__(self, size: tuple[float, float], with_parchment=True, pre_menu_event=None):
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
        self.captain_flip_image.set_position((size[0] // 2 - self.captain_flip_image.rect.w / 2, -size[1] // 20))
        self.sea_image.set_position((0, 0))

        # copy the images on the surface
        self.blit(self.sea_image, self.sea_image.rect.topleft)
        self.blit(self.captain_flip_image, self.captain_flip_image.rect.topleft)

        if with_parchment:
            # load parchment image
            self.parchment_image = Image(self, "assets/parchment.png", convert_alpha=True)

            # resize parchment
            scale_factor = (size[0] // 3) / self.parchment_image.rect.w
            self.parchment_image = self.parchment_image.resize(scale_factor)

            # set positions of the parchment
            self.parchment_image.set_position((size[0] // 2 - self.parchment_image.rect.w // 2,
                                               size[1] // 1.5 - self.parchment_image.rect.h // 2))

            # copy the image on the surface
            self.blit(self.parchment_image, self.parchment_image.rect.topleft)

        # add close button
        self.close_button = Button(self, "assets/buttons/x.png", call=lambda: (pygame.quit(), exit(0)),
                                   convert_alpha=True)
        self.close_button_hover = Image(self, "assets/buttons/x_hover.png", convert_alpha=True)
        scale_factor = (size[0] // 20) / self.close_button.rect.w
        self.close_button = self.close_button.resize(scale_factor)
        self.close_button_hover = self.close_button_hover.resize(scale_factor)
        self.close_button.set_position((size[0] - self.close_button.rect.w * 1.5, self.close_button.rect.h // 2))
        self.close_button_hover.set_position((size[0] - self.close_button.rect.w * 1.5, self.close_button.rect.h // 2))

        self.buttons.append(self.close_button)
        self.hover_dict[self.close_button.hashed] = self.close_button_hover
        self.blit(self.close_button, self.close_button.rect.topleft)

        if pre_menu_event is not None:
            self.backward_button = Button(self, "assets/buttons/left_arrow.png", call=lambda: pygame.event.post(
                pygame.event.Event(pre_menu_event)), convert_alpha=True)
            self.backward_button_hover = Image(self, "assets/buttons/left_arrow_hover.png", convert_alpha=True)
            scale_factor = (size[0] // 10) / self.backward_button.rect.w
            self.backward_button = self.backward_button.resize(scale_factor)
            self.backward_button_hover = self.backward_button_hover.resize(scale_factor)
            self.backward_button.set_position((self.backward_button.rect.w // 2, self.backward_button.rect.h // 2))
            self.backward_button_hover.set_position((self.backward_button.rect.w // 2,
                                                     self.backward_button.rect.h // 2))

            self.buttons.append(self.backward_button)
            self.hover_dict[self.backward_button.hashed] = self.backward_button_hover
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
        self.login_button = Button(self, "assets/buttons/login.png",
                                   call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_LOGIN)),
                                   convert_alpha=True)
        self.register_button = Button(self, "assets/buttons/register.png",
                                      call=lambda: pygame.event.post(pygame.event.Event(CHANGE_TO_REGISTER)),
                                      convert_alpha=True)
        self.quit_button = Button(self, "assets/buttons/quit.png", call=lambda: (pygame.quit(), exit(0)),
                                  convert_alpha=True)

        # load images for the hover effect
        self.login_button_hover = Image(self, "assets/buttons/login_hover.png", convert_alpha=True)
        self.register_button_hover = Image(self, "assets/buttons/register_hover.png", convert_alpha=True)
        self.quit_button_hover = Image(self, "assets/buttons/quit_hover.png", convert_alpha=True)

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
        self.gamemode_button = Button(self, "assets/buttons/gamemode.png", call=lambda: print("gamemode"),
                                      convert_alpha=True)
        self.stats_button = Button(self, "assets/buttons/stats.png", call=lambda: print("stats"), convert_alpha=True)
        self.quit_button = Button(self, "assets/buttons/quit.png", call=lambda: (pygame.quit(), exit(0)),
                                  convert_alpha=True)

        # load images for the hover effect
        self.gamemode_button_hover = Image(self, "assets/buttons/gamemode_hover.png", convert_alpha=True)
        self.stats_button_hover = Image(self, "assets/buttons/stats_hover.png", convert_alpha=True)
        self.quit_button_hover = Image(self, "assets/buttons/quit_hover.png", convert_alpha=True)

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
    def __init__(self, size, mode):
        super().__init__(size, pre_menu_event=CHANGE_TO_FIRST)

        self.db = Database("database.csv")
        self.mode = mode

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
        self.blit(self.sea_image, self.sea_image.rect.topleft)
        self.blit(self.captain_flip_image, self.captain_flip_image.rect.topleft)
        self.blit(self.parchment_image, self.parchment_image.rect.topleft)
        self.blit(self.close_button, self.close_button.rect.topleft)
        self.blit(self.backward_button, self.backward_button.rect.topleft)

        if mode == "login":
            # place login button
            self.login_button = Button(self, "assets/buttons/login.png", call=lambda: self.login(),
                                       convert_alpha=True)
            self.login_button_hover = Image(self, "assets/buttons/login_hover.png", convert_alpha=True)
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
            self.register_button = Button(self, "assets/buttons/register.png", call=lambda: self.register(),
                                          convert_alpha=True)
            self.register_button_hover = Image(self, "assets/buttons/register_hover.png", convert_alpha=True)
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

        if self.db.sign_in(username, password):
            print("logged in")
        else:
            print("wrong username or password")

        pygame.event.post(pygame.event.Event(CHANGE_TO_GAMEMODE))

    def register(self):
        username = self.input_box_username.text
        password = self.input_box_password.text

        self.db.sign_up(username, password)

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
        self.single_player_button = Button(self, "assets/buttons/single_player.png",
                                           call=lambda: print("single_player"), convert_alpha=True)
        self.multiplayer_button = Button(self, "assets/buttons/multiplayer.png",
                                         call=lambda: print("multiplayer"), convert_alpha=True)
        self.stats_button = Button(self, "assets/buttons/stats.png", call=lambda: print("stats"),
                                   convert_alpha=True)

        # load images for the hover effect
        self.single_player_button_hover = Image(self, "assets/buttons/single_player_hover.png", convert_alpha=True)
        self.multiplayer_button_hover = Image(self, "assets/buttons/multiplayer_hover.png", convert_alpha=True)
        self.stats_button_hover = Image(self, "assets/buttons/stats_hover.png", convert_alpha=True)

        # resize buttons
        scale_factor = (self.parchment_image.rect.w // 4.5) / 140
        self.single_player_button = self.single_player_button.resize(scale_factor)
        self.multiplayer_button = self.multiplayer_button.resize(scale_factor)
        self.stats_button = self.stats_button.resize(scale_factor)

        # resize hover effect
        self.single_player_button_hover = self.single_player_button_hover.resize(scale_factor)
        self.multiplayer_button_hover = self.multiplayer_button_hover.resize(scale_factor)
        self.stats_button_hover = self.stats_button_hover.resize(scale_factor)

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
    pass
