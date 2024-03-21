# creating a new class for the different columns composing the different boards
class Column:
    def __init__(self, length, bonus):
        self.column = []
        self.length = length
        self.bonus = bonus

    #Creating a function to add a new tile to the column
    def add_tile(self, tile):
    # Verifying the column's length
        if len(self.column) == self.length:
            pass
    # adding the tile to the column if the column isn't full
        else:
            self.column.append(tile)
            if len(self.column) == self.length:
            # applying the column's bonus if the column is full after adding the new tile
                self.apply_bonus(self.bonus)

    def apply_bonus(self):
        if self.bonus=="add3gold":
            pass








