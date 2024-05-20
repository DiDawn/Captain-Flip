from character import Character
import random
from tile_sprite import Tile


mapper = Character(0, "treasure_map", None)  # Done
navigator = Character(1, "navigator_act", None)  # Done
cooker = Character(2, "cooker_act", None)  # Done
gunboat = Character(3, "gunboat_act", "gunboat_end")  # Done
monkey = Character(4, "monkey_act", None)
parrot = Character(5, "parrot_act", "parrot_end")
cabin_boy = Character(6, None, "cabin_boy_end")  # Done
carpenter = Character(7, None, "no_gunners")
guard = Character(8, None, "on_top")

characters_list = [mapper, navigator, cooker, gunboat, monkey, parrot, cabin_boy, carpenter, guard]

tiles_path_dict = {
    0: "assets/tiles/mapper.png",
    1: "assets/tiles/navigator.png",
    2: "assets/tiles/cooker.png",
    3: "assets/tiles/gunboat.png",
    4: "assets/tiles/monkey.png",
    5: "assets/tiles/parrot.png",
    6: "assets/tiles/cabin_boy.png",
    7: "assets/tiles/carpenter.png",
    8: "assets/tiles/guard.png"
}


class TileManager:
    def __init__(self, character1, character2):
        self.character1 = character1
        self.character2 = character2

        self.active_character = character1

    def flip(self):
        self.active_character = self.character2 if self.active_character == self.character1 else self.character1


class Deck:
    def __init__(self, tile_size=(100, 100)):
        self.tile_size = tile_size
        self.deck = self.generate_deck()

    def draw(self):
        card = self.deck.pop(random.randint(0, len(self.deck) - 1))
        card.set_position((self.tile_size[0]/2, self.tile_size[1]/2))
        return card

    def generate_deck(self):
        pairs = [(i, j) for i in range(9) for j in range(9) if i != j]
        tiles = []
        for pair in pairs:
            character = characters_list[pair[0]]
            character_end = characters_list[pair[1]]
            tiles.append(Tile(self.tile_size, (tiles_path_dict[pair[0]], tiles_path_dict[pair[1]]), TileManager(character, character_end)))

        return tiles
