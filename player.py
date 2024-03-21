from database import Database

class Player:
    def __init__(self, board, id76):
        self.gold = 0
        self.boat_destroyed = False
        self.board = board
        self.id76 = id76
