from column import Column
from board import Board

B1C1 = Column(2, 1, 0, None)
B1C2 = Column(3, 2, 0, "treasure_map")
B1C3 = Column(5, 3, 0, "add5gold")
B1C4 = Column(2, 4, 2, None)
B1C5 = Column(3, 5, 0, "add3gold")

B2C1 = Column(2, 1, 0, "add1/0gold")
B2C2 = Column(3, 2, 0, "add2/1gold")
B2C3 = Column(5, 3, 0, "add6/3gold")
B2C4 = Column(1, 4, 0, "add0/2gold")
B2C5 = Column(4, 5, 0, "add4/2gold")

board1 = Board(1, B1C1, B1C2, B1C3, B1C4, B1C5)
board2 = Board(2, B2C1, B2C2, B2C3, B2C4, B2C5)


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
        self.treasure_map_possessor.gold += 1

    # function that examines if a player have his board full
    def end_of_the_game(self):
        for player in self.players_list:
            if player.board.verifying_full():
                return True
            else:
                return False
