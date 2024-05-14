from character import Character
import random
mapper = Character(1,"treasure_map", None) # Done
navigator = Character(2,"navigator_act",None) # Done
cooker = Character(3,"cooker_act", None) # Done
gunboat = Character(4,"gunboat_act", "gunboat_end") # Done
monkey = Character(5, "monkey_act", None)
parrot = Character(6, "parrot_act", "parrot_end")
cabin_boy = Character(7,None, "cabin_boy_end") # Done
carpenter= Character(8, None, None)
guard = Character(9, None, None)

characters_list = [mapper, navigator, cooker, gunboat, monkey, parrot, cabin_boy, carpenter, guard]
class Tile:
    def __init__(self):
        self.character = 0
        self.character_afk = 0
        self.tuple = [self.character, self.character_afk]
        self.x = -1
        self.y = -1
        self.pairs = ((i,j) for i in range(9) for j in range(9) if i !=j)

    # function to generate a tile with two different characters
    def tile_characters(self, characters_list):



# function to flip the cards
    def flip(self):
        save = self.character
        self.character = self.character_afk
        self.character_afk = save
