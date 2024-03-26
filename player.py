from database import Database


class Player:
    def __init__(self):
        self.gold = 0
        self.boat_destroyed = False
        self.board = None
        self.stats = (0, 0, 0)
