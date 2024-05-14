from tile_sprite import Tile
from board_pygame import Board
from parameters import *
from widgets import Button


class Game(pygame.Surface):
    def __init__(self, screen, screensize, board_number, players):
        super().__init__(screensize)

        self.screen = screen
        self.screensize = screensize
        self.screen_width, self.screen_height = screensize

        self.number_players = len(players)
        self.board_number = board_number

        self.boards = self.init_boards()
        self.players = players

        self.current_board = self.boards[0]

        # now pygame part
        self.flip_button = Button('assets/buttons/flip_button.png', convert_alpha=True)
        self.flip_button = self.flip_button.resize(2)
        self.flip_button.set_position((self.screen_width // 2 - self.flip_button.rect.w // 2,
                                       self.screen_height * 0.95 - self.flip_button.rect.h))

        self.blit(self.flip_button, self.flip_button.rect.topleft)

    def init_boards(self):
        return [Board((self.screen_height * 2 // 3, self.screen_height * 2 // 3), self.board_number)
                for _ in range(self.number_players)]

    def update_game_state(self):

        for board in self.boards:
            board.update()
            self.blit(board, board.rect.topleft)

        pygame.display.flip()
        if self.current_board.current_tile is None:
            self.current_board.current_tile = Tile((self.current_board.rect.w * 0.14, self.current_board.rect.h * 0.14),
                                                   ('assets/tiles/cabin_boy.png', 'assets/tiles/monkey.png'))

    def event_handler(self, event):
        if event:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.flip_button.rect.collidepoint(event.pos):
                    self.current_board.current_tile.flip()

            self.current_board.event_handler(event)

            self.update_game_state()
