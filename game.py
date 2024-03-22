from board import Board


class Game:
    def __init__(self, board, number_players):
        self.number_players = number_players
        self.board = board
        self.players_list = []
        self.end_game = False
        self.treasure_map_possessor = None
        self.add10_counter = 0
        self.add21_counter = 0
        self.add63_counter = 0
        self.add02_counter = 0
        self.add42_counter = 0

    # function that check who is the treasure's map possessor
    def map_possessor(self):
        self.treasure_map_possessor.gold +=1

    # function that examines if a player have his board full
    def end_of_the_game(self):
        for player in self.players_list:
            if player.board.verifying_full():
                return True
            else:
                return False
