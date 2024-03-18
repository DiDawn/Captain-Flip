import pygame
from pygame.locals import *
import ctypes
from resizer import resize


# init pygame module
pygame.init()


class HomeMenu(pygame.Surface):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)

        # load images for the background
        self.sea_image = pygame.image.load("sea.png").convert()
        self.captain_flip_image = pygame.image.load("captain_flip_logo.png").convert_alpha()

        # resize background image
        img_width = self.sea_image.get_size()[0]
        scale_factor = size[0] / img_width
        self.sea_image = resize(scale_factor, self.sea_image)

        # resize logo
        img_width = self.captain_flip_image.get_size()[0]
        scale_factor = (size[0] // 3) / img_width
        self.captain_flip_image = resize(scale_factor, self.captain_flip_image)

        # copy the images on the surface
        self.blit(self.sea_image, (0, 0))
        self.blit(self.captain_flip_image, (size[0]//2 - self.captain_flip_image.get_size()[0]//2, -size[1]//20))

        # load images for buttons
        self.parchment_image = pygame.image.load("parchment.png").convert_alpha()
        parchment_w, parchment_h = self.parchment_image.get_size()

        self.login_image = pygame.image.load("login.png").convert_alpha()

        # resize parchment
        img_width = self.parchment_image.get_size()[0]
        scale_factor = (size[0] // 3) / img_width
        self.parchment_image = resize(scale_factor, self.parchment_image)

        # resize login image
        img_width = self.login_image.get_size()[0]
        scale_factor = (parchment_w // 3) / img_width
        self.login_image = resize(scale_factor, self.login_image)

        # copy the images on the surface
        self.parchment_image.blit(self.login_image, (parchment_w//2 - self.login_image.get_size()[0] // 2,
                                                     parchment_h//4))

        # the image need to be blit at the end
        self.blit(self.parchment_image, (size[0] // 2 - self.captain_flip_image.get_size()[0] // 2,
                                         size[1] // 1.75 - self.captain_flip_image.get_size()[1] // 2))

    def event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # coordinates of click point.
            print(self.login_image.get_rect())
            if self.login_image.get_rect().collidepoint(mouse_pos):
                print('hi')


# get screen size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

background_colour = (0, 0, 0)
HOME_MENU = 0

# define dimension of pygame screen (width,height)
screen = pygame.display.set_mode(screensize)

# Set the caption of the screen
pygame.display.set_caption('Captain FLip')

# Fill the background colour to the screen
screen.fill(background_colour)

# Update the display using flip
pygame.display.flip()

# init home_screen
home_menu = HomeMenu(screensize)
game_state = HOME_MENU

# Variable to keep our game loop running
running = True

# game loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
        else:
            if game_state == HOME_MENU:
                home_menu.event_handler(event)

    screen.blit(home_menu, (0, 0))
    pygame.display.flip()
