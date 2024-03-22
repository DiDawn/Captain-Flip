from database import Database


class Player:
    def __init__(self, board, ID):
        self.gold = 0
        self.boat_destroyed = False
        self.board = board
