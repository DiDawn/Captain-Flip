from board import Board


class Game:
    def __init__(self, board, number_players):
        self.treasure_map_possessor = None
        self.players_list = []
        self.number_players = number_players
        self.board = board
        self.add10_counter = 0
        self.add21_counter = 0
        self.add63_counter = 0
        self.add02_counter = 0
        self.add42_counter = 0

    # function that check who is the treasure's map possessor
    def card_possessor(self):
        # browse the list of players
        for player in self.players_list:
            # if it's identical, then the associated player possess the map for the turn
            if self.treasure_map_possessor == player.id76:
                # it adds a gold to the possessor
                player.gold += 1
