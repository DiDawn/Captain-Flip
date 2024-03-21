from column import Column

# yes
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
        self.board = list[column1, column2, column3, column4, column5]
