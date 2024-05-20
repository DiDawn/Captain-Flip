from player import Player


# creating a new class for the different columns composing the different boards
class Column:

    def __init__(self, length, place_in_the_board, gap_from_the_bottom, effect):
        self.column = []
        self.length = length
        self.place_in_the_board = place_in_the_board
        self.gap_from_the_bottom = gap_from_the_bottom
        self.effect = effect

    # Creating a function to add a new tile to the column
    def add_tile(self, tile, player, game):
        # checking if the column is already full
        if len(self.column) == self.length:
            # returning False to indicate that the column is full and the action is impossible
            return False
        else:
            # adding the tile to the column
            self.column.append(tile)
            # if the column is full after that addition, it applies the effect of the column
            if len(self.column) == self.length:
                self.apply_bonus(player, game)
            # returning True to indicate that the addition was successfully done
            return True

    def same_character(self):
        if len(self.column) == 0:
            return False
        else:
            for i in range(1, len(self.column)):
                if self.column[i].tile_manager.active_character.character_id != self.column[i - 1].tile_manager.active_character.character_id:
                    return False
            return True

    def different_characters(self):
        # return True if the column is filled with all different characters
        if len(self.column) == 0:
            return False
        else:
            for i in range(1, len(self.column)):
                for j in range(i):
                    if self.column[i].tile_manager.active_character.character_id == self.column[j].tile_manager.active_character.character_id:
                        return False
            return True

# verifying if there is a cabin boy in the column
    def cabin_boy_aboard(self):
        cabin_boy_presence = 0
        for tile in self.column:
            if tile.tile_manager.active_character.character_id == 6:
                cabin_boy_presence += 1
        return cabin_boy_presence

    def is_full(self):
        return len(self.column) == self.length

    def __getitem__(self, item):
        return self.column[item]

    def __iadd__(self, other):
        self.column.append(other)
        return self
