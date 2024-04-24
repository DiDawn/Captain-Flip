from database import Database


class Player:
    def __init__(self,board):
        self.gold = 0
        self.boat_destroyed = False
        self.board = board
        self.stats = (0, 0, 0)
