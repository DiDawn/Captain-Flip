from column import Column

B1C1 = Column(2, 0, 0, None)
B1C2 = Column(3, 1, 0, "treasure_map")
B1C3 = Column(5, 2, 0, "add5gold")
B1C4 = Column(2, 3, 2, None)
B1C5 = Column(3, 4, 0, "add3gold")
BOARD1COLUMNS = [B1C1, B1C2, B1C3, B1C4, B1C5]

B2C1 = Column(2, 0, 0, "add1/0gold")
B2C2 = Column(3, 1, 0, "add2/1gold")
B2C3 = Column(5, 2, 0, "add6/3gold")
B2C4 = Column(1, 3, 0, "add0/2gold")
B2C5 = Column(4, 4, 0, "add4/2gold")
BOARD2COLUMNS = [B2C1, B2C2, B2C3, B2C4, B2C5]

BOARDS_COLUMNS = [BOARD1COLUMNS, BOARD2COLUMNS]


class BoardManager:
    def __init__(self, board_number):
        self.columns = BOARDS_COLUMNS[board_number]
        self.highest_column = 5 if board_number != 4 else 4
        self.rows = [[None] * 5 for _ in range(self.highest_column)]

    def insert_tile(self, column_number, tile):
        column = self.columns[column_number]
        if column.is_full():
            return False
        column.column.append(tile)
        self.rows[len(self.rows) - len(column.column) - column.gap_from_the_bottom][column_number] = tile
        print("-----------------------")
        print("\n".join(str(row) for row in self.rows))
        print("-----------------------")
        return True

    # return the height of the first empty tile in the columns
    def get_empty_tiles(self):
        empty_tiles = []
        for column in self.columns:
            length = len(column.column)
            if length < column.length:
                empty_tiles.append(length)
            else:
                empty_tiles.append(None)
        return empty_tiles

    def cabin_boy_aboard(self):
        cabin_boy_counter = 0
        for column in self.columns:
            cabin_boy_counter += column.cabin_boy_aboard()
        return cabin_boy_counter

    def gunboat_aboard(self):
        gunboat_counter = 0
        for column in self.columns:
            for tile in column:
                if tile.character.character_id == 4:
                    gunboat_counter += 1
        return gunboat_counter

    # check if at least 3 columns are filled
    def check_end(self):
        filled_columns = 0
        for column in self.columns:
            if column.is_full():
                filled_columns += 1
