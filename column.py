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

    # Creating a function to apply a bonus when a column is full (if there is a bonus)
    def apply_bonus(self, player, game):
        if self.effect == "add3gold":
            player.gold += 3
        elif self.effect == "add5gold":
            player.gold += 5
        elif self.effect == "treasure_map":
            # letting the game know who is the possessor of the map
            game.treasure_map_possessor = player
        elif self.effect == "add1/0gold":
            # the first person to finish that column win 1 gold
            if game.add10_counter == 0:
                player.gold += 1
            # The other players wins 0 gold if they finish that column
            else:
                pass
            # letting the game know that the column has been filled by a player at least once
            game.add10_counter += 1
        elif self.effect == "add2/1gold":
            # the first person to finish that column win 2 gold
            if game.add21_counter == 0:
                player.gold += 2
            # The other players wins 1 gold if they finish that column
            else:
                player.gold += 1
            # letting the game know that the column has been filled by a player at least once
            game.add21_counter += 1
        elif self.effect == "add6/3gold":
            # the first person to finish that column win 6 gold
            if game.add63_counter == 0:
                player.gold += 6
            # The other players wins 3 gold if they finish that column
            else:
                player.gold += 3
            # letting the game know that the column has been filled by a player at least once
            game.add63_counter += 1
        elif self.effect == "add0/2gold":
            # the first person to finish that column win 0 gold
            if game.add02_counter == 0:
                pass
            # The other players wins 2 gold if they finish that column
            else:
                player.gold += 2
            # letting the game know that the column has been filled by a player at least once
            game.add02_counter += 1
        elif self.effect == "add4/2gold":
            # the first person to finish that column win 4 gold
            if game.add42_counter == 0:
                player.gold += 4
            # The other players wins 2 gold if they finish that column
            else:
                player.gold += 2
            # letting the game know that the column has been filled by a player at least once
            game.add42_counter += 1
        else:
            pass

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
