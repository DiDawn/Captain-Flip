import pygame


class SoundEffects:
    def __init__(self):
        self.sounds_effects = {}

    def init_sound_effects(self, sound_effects: list[str]):
        for sound_effect in sound_effects:
            self.sounds_effects[sound_effect] = pygame.mixer.Sound(f'assets/music/sound_effects/{sound_effect}.ogg')
            self.sounds_effects[sound_effect].set_volume(0.1)

    def play(self, sound_effect: str):
        self.sounds_effects[sound_effect].play()
