from tile import Tile

class Character:
    def __init__(self, character_id, active_effect, end_effect):
        self.character_id = character_id
        self.active_effect = active_effect
        self.end_effect = end_effect

    def active_effect(self, player, game, board, floor_of_the_row, position_in_the_row):
        if self.active_effect == "treasure_map":
            # letting the game know who is the possessor of the map
            game.treasure_map_possessor = player
        # for the "cannonière"
        if self.active_effect == "gunboat_act":
            player.gold += 5
        if self.active_effect == "cooker_act":
            # Adding to the player an amount of gold equal to the number of characters there are already in the row
            # where the cooker is placed in by counting him (+1)
            player.gold += len(board.row_list[floor_of_the_row-1]) + 1






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


mapper = Character(1,"treasure_map", None)
navigator = Character(2,None,None)
cooker = Character(3,"cooker_act", None)
gunboat = Character(4,"gunboat_act", "gunboat_end")
monkey = Character(5, None, None)
parrot = Character(6, None, None)
cabin_boy = Character(7,None, "cabin_boy_end")
carpenter= Character(8, None, None)
guard = Character(9, None, None)



