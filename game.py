from column import Column
from board import Board
from tile import Tile
from character import Character
from random import shuffle

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

board1 = Board(1, B1C1, B1C2, B1C3, B1C4, B1C5)
board2 = Board(2, B2C1, B2C2, B2C3, B2C4, B2C5)

mapper = Character(1, "treasure_map", None)
navigator = Character(2, None, None)
cooker = Character(3, "cooker_act", None)
gunboat = Character(4, "gunboat_act", "gunboat_end")
monkey = Character(5, None, None)
parrot = Character(6, None, None)
cabin_boy = Character(7, None, "cabin_boy_end")
carpenter = Character(8, None, None)
guard = Character(9, None, None)


class Game:
    def __init__(self, board, number_players,players_list):
        self.number_players = number_players
        self.board = board
        self.players_list = players_list
        self.end_game = False
        self.treasure_map_possessor = None
        self.add10_counter = 0
        self.add21_counter = 0
        self.add63_counter = 0
        self.add02_counter = 0
        self.add42_counter = 0

    # function that check who is the treasure's map possessor
    def map_possessor(self):
        self.treasure_map_possessor.gold += 1

    # function that examines if a player have his board full
    def end_of_the_game(self):
        for player in self.players_list:
            if player.board.verifying_full():
                self.end_game = True
            else:
                self.end_game = False

    def game_running(self):
        # randomizing player's order
        shuffle(self.players_list)
        turn = 0
        current_player = 0
        # the game run until at least a player's board is full
        while not self.end_game:
            # the game decides whose turn it is
            current_player = self.players_list[turn % self.number_players]
            turn += 1
            # generates a new tile with random characters
            tile = Tile()
            tile.random_characters(mapper, navigator, cooker, gunboat, monkey, parrot, cabin_boy, carpenter, guard)
            # activates character effect when he is placed
            tile.character.active_effect(current_player, Game, tile)

            for player in self.players_list:
                if self.treasure_map_possessor == player:
                    player.gold += 1
                else:
                    pass
