from database import Database


class Player:
    def __init__(self, stats):
        self.gold = 0
        self.boat_destroyed = False
        self.board = None
        self.stats = stats
