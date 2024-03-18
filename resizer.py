import pygame
from pygame.transform import scale


def resize(scale_factor: float | int, surface: pygame.Surface) -> pygame.Surface:
    w, h = surface.get_size()
    new_w, new_h = w * scale_factor, h * scale_factor
    return scale(surface, [new_w, new_h])
