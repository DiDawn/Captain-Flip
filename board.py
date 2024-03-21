from column import Column

B1C1 = Column(2, None)
B1C2 = Column(3, "treasure_map")
B1C3 = Column(5, "add5gold")
B1C4 = Column(2, None)
B1C5 = Column(3, "add3gold")

B2C1 = Column(2, "add1/0gold")
B2C2 = Column(3, "add2/1gold")
B2C3 = Column(5, "add6/3gold")
B2C4 = Column(1, "add0/2gold")
B2C5 = Column(4, "add4/2gold")


class Board:
    def __init__(self, column1, column2, column3, column4, column5):
        self.column_list = [column1, column2, column3, column4, column5]
        self.full_column_counter = 0

    # function to verify if the board is full
    def verifying_full(self):
        for column in self.column_list:
            # verifying if every column composing the board is full
            if len(column) == column.lenght:
                self.full_column_counter += 1
            # if the board is full then it returns True to indicate the end of the game
            if self.full_column_counter == 5:
                return True
            # if the board is not full then it returns False, the game continues
            else:
                return False
