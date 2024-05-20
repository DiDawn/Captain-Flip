from database import Database


class Player:
    def __init__(self, username):
        self.username = username
        self.gold = 0
        self.boat_destroyed = False
        self.stats = (0, 0, 0)
        self.map_possessor = False

    def __str__(self):
        return (f"Player {self.username} has {self.gold} gold and is {'not ' if not self.map_possessor else ''}the map "
                f"possessor.")

    def reset(self):
        self.gold = 0
        self.boat_destroyed = False
        self.map_possessor = False
