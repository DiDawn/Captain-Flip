from column import Column

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


class Board:
    def __init__(self, number, column1, column2, column3, column4, column5):
        self.column_list = [column1, column2, column3, column4, column5]
        self.number = number
        self.full_column_counter = 0
        self.gunboat_counter = 0
        self.cabin_boy_on_board_counter = 0
        self.row1 = []
        self.row2 = []
        self.row3 = []
        self.row4 = []
        self.row5 = []
        self.row_list = []

# creating a function to generate rows on the board
    def generates_rows(self):
        # Loop through each column in the columns list
        for column in self.column_list:
            # Check the gap from the bottom for each column and append data to the corresponding row
            # If the gap from the bottom is 0
            if column.gap_from_the_bottom == 0:
                # Append the first tile of the column to row 1
                self.row1.append(column[0])
                if column.lenght > 1:
                    # If column length > 1, append the second tile of the column to row 2
                    self.row2.append(column[1])
                    if column.lenght > 2:
                        # If column length > 2, append the third tile of the column to row 3
                        self.row3.append(column[2])
                        if column.lenght > 3:
                            # If column length > 3, append the fourth tile of the column to row 4
                            self.row4.append(column[3])
                            if column.lenght > 4:
                                # If column length > 4, append the fifth tile of the column to row 5
                                self.row5.append(column[4])
            if column.gap_from_the_bottom == 1:
                # If the gap from the bottom is 1
                self.row2.append(column[0])
                # Append the first tile of the column to row 2
                if column.lenght > 1:
                    # If column length > 1, append the second tile of the column to row 3
                    self.row3.append(column[1])
                    if column.lenght > 2:
                        # If column length > 2, append the third tile of the column to row 4
                        self.row4.append(column[2])
                        if column.lenght > 3:
                            # If column length > 2, append the fourth tile of the column to row 5
                            self.row5.append(column[3])
            if column.gap_from_the_bottom == 2:
                # If the gap from the bottom is 2
                self.row3.append(column[0])
                # Append the first tile of the column to row 3
                if column.lenght > 1:
                    # If column length > 1, append the second tile of the column to row 4
                    self.row4.append(column[1])
                    if column.lenght > 2:
                        # If column length > 2, append the third tile of the column to row 5
                        self.row5.append(column[2])
            if column.gap_from_the_bottom == 3:
                # If the gap from the bottom is 3
                self.row4.append(column[0])
                # Append the first tile of the column to row 4
                if column.lenght > 1:
                    # If column length > 1, append the second tile of the column to row 5
                    self.row5.append(column[1])
            if column.gap_from_the_bottom == 4:
                # If the gap from the bottom is 3
                self.row5.append(column[0])
                # Append the first tile of the column to row 5

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

# creating a function to calculate how many column have at least a mousse
    def counting_columns_with_a_cabin_boy_on_board(self):
        for column in self.column_list:
            self.cabin_boy_on_board_counter += column.cabin_boy_presence
            return self.cabin_boy_on_board_counter

# creating a function to calculate how many gunboat you have on a boat
    def gunboat_counter(self):
        for column in self.column_list:
            for tile in column:
                if tile.character.character_id == 4:
                    self.gunboat_counter += 1
        return self.gunboat_counter

