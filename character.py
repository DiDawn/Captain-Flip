from tile import Tile


class Character:
    def __init__(self, character_id, active_effect, end_effect):
        self.character_id = character_id
        self.active_effect = active_effect
        self.end_effect = end_effect

    def active_effect(self, player, game, tile):
        if self.active_effect == "treasure_map":
            # letting the game know who is the possessor of the map
            game.treasure_map_possessor = player
        if self.active_effect == "gunboat_act":
            player.gold += 5
        if self.active_effect == "cooker_act":
            # Adding to the player an amount of gold equal to the number of characters there are already in the row
            # where the cooker is placed in by counting him (+1)
            player.gold += len(player.board.row_list[tile.y-1]) + 1
        if self.active_effect == "navigator_act":
            counter = 0
            # counting the number of mapper on the current player's board
            for column in player.board.column_list:
                for tile in column:
                    if tile.character == mapper:
                        counter += 1
            # adding 2 golds to the current player for every mapper on his board
            player.gold += 2*counter
        if self.active_effect == "monkey_act":
            player.gold += 1

            if tile.x == 0:

            # flip the tile above the monkey
            player.board.column_list[tile.x][tile.y + 1].flip()
            # flip the tile under the monkey
            player.board.column_list[tile.x][tile.y - 1].flip()
            # flip the tile at the right of the monkey
            player.board.row_list[tile.y][tile.x + 1].flip()
            # flip the tile at the left of the monkey
            player.board.row_list[tile.y][tile.x - 1].flip()




    def end_effect(self, player, game, board):
        if self.end_effect == "gunboat_end":
            board.gunboat_counter += 1
        if self.end_effect == "parrot_end":
            player.gold += -1
        if self.end_effect == "cabin_boy_end":
            if board.cabin_boy_on_board_counter == 5:
                player.gold += 25
            if board.cabin_boy_on_board_counter == 4:
                player.gold += 16
            if board.cabin_boy_on_board_counter == 3:
                player.gold += 9
            if board.cabin_boy_on_board_counter == 2:
                player.gold += 4
            if board.cabin_boy_on_board_counter == 1:
                player.gold += 1


mapper = Character(1,"treasure_map", None) # Done
navigator = Character(2,"navigator_act",None) # Done
cooker = Character(3,"cooker_act", None) # Done
gunboat = Character(4,"gunboat_act", "gunboat_end") # Done
monkey = Character(5, "monkey_act", None)
parrot = Character(6, None, None)
cabin_boy = Character(7,None, "cabin_boy_end") # Done
carpenter= Character(8, None, None)
guard = Character(9, None, None)



