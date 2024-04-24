from character import Character
import random


class Tile:
    def __init__(self):
        self.character = 0
        self.character_afk = 0
        self.tuple = [self.character, self.character_afk]
        self.x = -1
        self.y = -1

    # function to generate a tile with two different characters
    def random_characters(self, mapper, navigator, cooker, gunboat, monkey, parrot, cabin_boy, carpenter, guard):
        self.character = random.randint(1, 9)
        self.character_afk = random.randint(1, 9)
        # making sure that the two characters are different
        if self.character == self.character_afk:
            while self.character == self.character_afk:
                self.character_afk = random.randint(1, 9)
        # associating an active character according to the number we drew
        if self.character == 1:
            self.character = mapper
        elif self.character == 2:
            self.character = navigator
        elif self.character == 3:
            self.character = cooker
        elif self.character == 4:
            self.character = gunboat
        elif self.character == 5:
            self.character = monkey
        elif self.character == 6:
            self.character = parrot
        elif self.character == 7:
            self.character = cabin_boy
        elif self.character == 8:
            self.character = carpenter
        elif self.character == 9:
            self.character = guard
        # associating an afk character according to the number we drew
        if self.character_afk == 1:
            self.character_afk = mapper
        elif self.character_afk == 2:
            self.character_afk = navigator
        elif self.character_afk == 3:
            self.character_afk = cooker
        elif self.character_afk == 4:
            self.character_afk = gunboat
        elif self.character_afk == 5:
            self.character_afk = monkey
        elif self.character_afk == 6:
            self.character_afk = parrot
        elif self.character_afk == 7:
            self.character_afk = cabin_boy
        elif self.character_afk == 8:
            self.character_afk = carpenter
        elif self.character_afk == 9:
            self.character_afk = guard

# function to flip the cards
    def flip(self):
        save = self.character
        self.character = self.character_afk
        self.character_afk = save
