from column import Column
from parameters import *

B0C0 = Column(2, 0, 0, None)
B0C1 = Column(3, 1, 0, "treasure_map")
B0C2 = Column(5, 2, 0, "add5gold")
B0C3 = Column(2, 3, 2, None)
B0C4 = Column(3, 4, 0, "add3gold")
BOARD0COLUMNS = [Column(2, 0, 0, None),
                 Column(3, 1, 0, "treasure_map"),
                 Column(5, 2, 0, "add5gold"),
                 Column(2, 3, 2, None),
                 Column(3, 4, 0, "add3gold")]

B1C0 = Column(2, 0, 0, "add1/0gold")
B1C1 = Column(3, 1, 0, "add2/1gold")
B1C2 = Column(5, 2, 0, "add6/3gold")
B1C3 = Column(1, 3, 0, "add0/2gold")
B1C4 = Column(4, 4, 0, "add4/2gold")
BOARD1COLUMNS = [Column(2, 0, 0, "add1/0gold"),
                 Column(3, 1, 0, "add2/1gold"),
                 Column(5, 2, 0, "add6/3gold"),
                 Column(1, 3, 0, "add0/2gold"),
                 Column(4, 4, 0, "add4/2gold")]

B2C0 = Column(3, 0, 0, "treasure_map")
B2C1 = Column(3, 1, 0, "same_crew")
B2C2 = Column(2, 2, 0, None)
B2C3 = Column(5, 3, 0, "different_crew")
B2C4 = Column(2, 4, 0, None)
BOARD2COLUMNS = [Column(3, 0, 0, "treasure_map"),
                 Column(3, 1, 0, "same_crew"),
                 Column(2, 2, 0, None),
                 Column(5, 3, 0, "different_crew"),
                 Column(2, 4, 0, None)]

B3C0 = Column(3, 0, 1, "add3gold")
B3C1 = Column(4, 1, 0, "2gold_per_filled_column")
B3C2 = Column(5, 2, 0, "1gold_per_different_character")
B3C3 = Column(2, 3, 2, None)
B3C4 = Column(1, 4, 2, None)
BOARD3COLUMNS = [Column(3, 0, 1, "add3gold"),
                 Column(4, 1, 0, "2gold_per_filled_column"),
                 Column(5, 2, 0, "1gold_per_different_character"),
                 Column(2, 3, 2, None),
                 Column(1, 4, 2, None)]

B4C0 = Column(4, 0, 0, "add4gold")
B4C1 = Column(2, 1, 0, "take_map_if_same_crew")
B4C2 = Column(3, 2, 0, "flip_any_tile_if_different_crew")
B4C3 = Column(3, 3, 0, "draw_new_card_if_same_crew")
B4C4 = Column(3, 4, 1, "add3gold")
BOARD4COLUMNS = [Column(4, 0, 0, "add4gold"),
                 Column(2, 1, 0, "take_map_if_same_crew"),
                 Column(3, 2, 0, "flip_any_tile_if_different_crew"),
                 Column(3, 3, 0, "draw_new_card_if_same_crew"),
                 Column(3, 4, 1, "add3gold")]


class BoardManager:
    def __init__(self, board_number, player, players):
        self.board_number = board_number
        self.columns = self.generate_columns()
        self.highest_column = 5 if board_number != 4 else 4
        self.rows = [[None] * 5 for _ in range(self.highest_column)]
        self.player = player
        self.mode = "solo" if len(players) == 1 else "multi"
        self.players = players
        self.columns_active_effects_used = [False] * 5
        self.column3_already_filled = False
        if self.mode == "solo":
            self.solo_column_completion = 0

    def generate_columns(self):
        if self.board_number == 0:
            return [Column(2, 0, 0, None),
                    Column(3, 1, 0, "treasure_map"),
                    Column(5, 2, 0, "add5gold"),
                    Column(2, 3, 2, None),
                    Column(3, 4, 0, "add3gold")]

        elif self.board_number == 1:
            return [Column(2, 0, 0, "add1/0gold"),
                    Column(3, 1, 0, "add2/1gold"),
                    Column(5, 2, 0, "add6/3gold"),
                    Column(1, 3, 0, "add0/2gold"),
                    Column(4, 4, 0, "add4/2gold")]

        elif self.board_number == 2:
            return [Column(3, 0, 0, "treasure_map"),
                    Column(3, 1, 0, "same_crew"),
                    Column(2, 2, 0, None),
                    Column(5, 3, 0, "different_crew"),
                    Column(2, 4, 0, None)]

        elif self.board_number == 3:
            return [Column(3, 0, 1, "add3gold"),
                    Column(4, 1, 0, "2gold_per_filled_column"),
                    Column(5, 2, 0, "1gold_per_different_character"),
                    Column(2, 3, 2, None),
                    Column(1, 4, 2, None)]

        elif self.board_number == 4:
            return [Column(4, 0, 0, "add4gold"),
                    Column(2, 1, 0, "take_map_if_same_crew"),
                    Column(3, 2, 0, "flip_any_tile_if_different_crew"),
                    Column(3, 3, 0, "draw_new_card_if_same_crew"),
                    Column(3, 4, 1, "add3gold")]

    def insert_tile(self, column_number, tile):
        column = self.columns[column_number]
        if column.is_full():
            return False

        x = column_number
        y = len([tile for tile in column.column if tile is not None]) + column.gap_from_the_bottom
        tile.set_pos_in_grid((x, y))

        column.column.append(tile)
        self.rows[len(self.rows) - len(column.column) - column.gap_from_the_bottom][column_number] = tile

        print("-----------------------")
        print("\n".join(str(row) for row in self.rows))
        print("-----------------------")

        # apply the active effect of the character
        self.apply_active_effect(tile)

        con1 = tile.tile_manager.active_character.character_id != 4
        con2 = tile.tile_manager.active_character.character_id != 5
        con3 = self.board_number == 4 and column_number == 3 and self.columns[3].is_full() and not self.column3_already_filled
        if con1 and con2 and not con3:
            pygame.event.post(pygame.event.Event(END_TURN))
        if tile.tile_manager.active_character.character_id == 5:
            pygame.event.post(pygame.event.Event(PARROT_ACT))

        if self.columns[column_number].is_full():
            self.apply_column_effects(column_number)

        print(self.player)

        return True

    def apply_active_effect(self, tile):
        active_character = tile.tile_manager.active_character
        active_effect = active_character.active_effect

        if active_effect == "treasure_map":
            if self.mode == "multi":
                for player in self.players:
                    player.map_possessor = False
                self.player.map_possessor = True
            else:
                self.player.map_possessor = True if self.player.map_possessor is False else False

        if active_effect == "gunboat_act":
            self.player.gold += 5

        if active_effect == "cooker_act":
            y = tile.y
            y = self.highest_column - y - 1
            self.player.gold += len([tile for tile in self.rows[y] if tile is not None])

        if active_effect == "navigator_act":
            self.player.gold += 2 * self.mapper_aboard()

        if active_effect == "monkey_act":
            flippable_tiles = self.tiles_around(tile.x, tile.y)
            pygame.event.post(pygame.event.Event(MONKEY_ACT, tiles_pos=flippable_tiles))

    # return the height of the first empty tile in the columns
    def get_empty_tiles(self):
        empty_tiles = []
        for column in self.columns:
            length = len(column.column)
            if length < column.length:
                empty_tiles.append(length)
            else:
                empty_tiles.append(None)
        return empty_tiles

    def cabin_boy_aboard(self):
        cabin_boy_counter = 0
        for column in self.columns:
            if column.cabin_boy_aboard() > 0:
                cabin_boy_counter += 1
        return cabin_boy_counter

    def gunboat_aboard(self):
        gunboat_counter = 0
        for column in self.columns:
            for tile in column:
                if tile.tile_manager.active_character.character_id == 3:
                    gunboat_counter += 1
        return gunboat_counter

    def mapper_aboard(self):
        mapper_counter = 0
        for column in self.columns:
            for tile in column:
                if tile.tile_manager.active_character.character_id == 0:
                    mapper_counter += 1
        return mapper_counter

    def parrot_aboard(self):
        parrot_counter = 0
        for column in self.columns:
            for tile in column:
                if tile.tile_manager.active_character.character_id == 5:
                    parrot_counter += 1
        return parrot_counter

    def tiles_around(self, x, y):
        positions = []
        if x > 0:
            positions.append((x-1, y))
        if x < 4:
            positions.append((x+1, y))
        if y > 0:
            positions.append((x, y-1))
        if y < self.highest_column - 1:
            positions.append((x, y+1))
        valid_positions = []

        for pos in positions:
            if self.rows[self.highest_column - pos[1] - 1][pos[0]] is not None:
                valid_positions.append(pos)

        return valid_positions

    def monkey_flip(self, tile):
        if tile is not None:
            tile.monkey_flip()
            self.apply_active_effect(tile)
            pygame.event.post(pygame.event.Event(END_TURN))

    def apply_column_effects(self, column_number):
        effect = self.columns[column_number].effect

        if effect == "treasure_map":
            if self.mode == "multi":
                for player in self.players:
                    player.map_possessor = False
                self.player.map_possessor = True
            else:
                self.player.map_possessor = True if self.player.map_possessor is False else False

        elif effect == "add5gold":
            self.player.gold += 5

        elif effect == "add3gold":
            self.player.gold += 3

        elif effect == "add4gold":
            self.player.gold += 4

        elif effect == "add1/0gold":
            if self.mode == "multi":
                if self.columns_active_effects_used[column_number]:
                    self.player.gold += 0
                else:
                    self.player.gold += 1
            else:
                if self.solo_column_completion < 3:
                    self.player.gold += 1

        elif effect == "add2/1gold":
            if self.mode == "multi":
                if self.columns_active_effects_used[column_number]:
                    self.player.gold += 1
                else:
                    self.player.gold += 2
            else:
                if self.solo_column_completion < 3:
                    self.player.gold += 2
                else:
                    self.player.gold += 1

        elif effect == "add6/3gold":
            if self.mode == "multi":
                if self.columns_active_effects_used[column_number]:
                    self.player.gold += 3
                else:
                    self.player.gold += 6
            else:
                if self.solo_column_completion < 3:
                    self.player.gold += 6
                else:
                    self.player.gold += 3

        elif effect == "add0/2gold":
            if self.mode == "multi":
                if self.columns_active_effects_used[column_number]:
                    self.player.gold += 2
                else:
                    self.player.gold += 0
            else:
                if self.solo_column_completion < 3:
                    self.player.gold += 0
                else:
                    self.player.gold += 2

        elif effect == "add4/2gold":
            if self.mode == "multi":
                if self.columns_active_effects_used[column_number]:
                    self.player.gold += 2
                else:
                    self.player.gold += 4
            else:
                if self.solo_column_completion < 3:
                    self.player.gold += 4
                else:
                    self.player.gold += 2

        elif effect == "same_crew":
            if self.columns[column_number].same_character():
                self.player.gold += 6

        elif effect == "different_crew":
            if self.columns[column_number].different_characters():
                self.player.gold += 4

        elif effect == "2gold_per_filled_column":
            filled_columns = 0
            for column in self.columns:
                if column.is_full():
                    filled_columns += 1
            self.player.gold += 2 * filled_columns

        elif effect == "1gold_per_different_character":
            column = self.columns[column_number]
            characters_ids = set()
            for tile in column.column:
                if tile is not None:
                    characters_ids.add(tile.tile_manager.active_character.character_id)
            self.player.gold += len(characters_ids)

        elif effect == "take_map_if_same_crew":
            if self.columns[column_number].same_character():
                if self.mode == "multi":
                    for player in self.players:
                        player.map_possessor = False
                    self.player.map_possessor = True
                else:
                    self.player.map_possessor = True if self.player.map_possessor is False else False

        elif effect == "flip_any_tile_if_different_crew":
            if self.columns[column_number].different_characters():
                flippable_tiles = []
                for column in self.columns:
                    for tile in column.column:
                        if tile is not None:
                            flippable_tiles.append((tile.x, tile.y))
                pygame.event.post(pygame.event.Event(MONKEY_ACT, tiles_pos=flippable_tiles))

        elif effect == "draw_new_card_if_same_crew":
            if self.columns[column_number].same_character():
                self.column3_already_filled = True
                pygame.event.post(pygame.event.Event(PARROT_ACT))

        pygame.event.post(pygame.event.Event(COLUMN_ACTIVE_EFFECT_USED, column_number=column_number))

    # check if at least 4 columns are filled
    def check_end(self):
        filled_columns = 0
        for column in self.columns:
            if column.is_full():
                filled_columns += 1

        if filled_columns >= 4:
            pygame.event.post(pygame.event.Event(BOARD_FINISHED))

    def apply_end_effects(self):
        print("-----------------------")
        print(f"applying end effects for {self.player.username}")
        for column in self.columns:
            for tile in column.column:
                if tile is not None:

                    active_character = tile.tile_manager.active_character
                    end_effect = active_character.end_effect

                    if end_effect == "parrot_end":
                        if self.player.gold > 0:
                            self.player.gold -= 1
                            print(f"{self.player.username} lost 1 gold because of the parrot")

                    if end_effect == "gunboat_end":
                        if self.gunboat_aboard() > 2:
                            self.player.boat_destroyed = True
                            print(f"{self.player.username} lost the game because of the gunboat")

                    if end_effect == "on_top":
                        if tile.y == len(column.column) - 1 - column.gap_from_the_bottom:
                            self.player.gold += 4
                            print(f"{self.player.username} earned 4 gold because a guard was on top of the column")

                    if end_effect == "no_gunners":
                        gunners_in_column = 0
                        for tile_column in column.column:
                            if tile_column.tile_manager.active_character.character_id == 3:
                                gunners_in_column += 1
                        gunners_in_row = 0
                        y = self.highest_column - tile.y - 1
                        for tile_row in self.rows[y]:
                            if tile_row is not None:
                                if tile_row.tile_manager.active_character.character_id == 3:
                                    gunners_in_row += 1
                        if gunners_in_column + gunners_in_row == 0:
                            self.player.gold += 3
                            print(f"{self.player.username} earned 3 gold because there were no gunners in the column")
                        else:
                            print(f"{self.player.username} didn't earn gold because there were gunners in the column or row")

        reward_per_cabin_boy = [1, 4, 9, 16, 25]
        cabin_boy_aboard = self.cabin_boy_aboard()
        print(f"{self.player.username} has {cabin_boy_aboard} cabin ans will earn {reward_per_cabin_boy[cabin_boy_aboard - 1]} gold")
        if cabin_boy_aboard > 0:
            self.player.gold += reward_per_cabin_boy[cabin_boy_aboard - 1]
        print("-----------------------")
