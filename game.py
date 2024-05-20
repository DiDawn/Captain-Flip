from board_pygame import Board
from parameters import *
from widgets import Button
from deck import Deck


class Game(pygame.Surface):
    def __init__(self, screen, screensize, board_number, players):
        super().__init__(screensize)

        self.screen = screen
        self.screensize = screensize
        self.screen_width, self.screen_height = screensize

        self.background = pygame.image.load('assets/sea.png')

        self.number_players = len(players)

        self.board_number = board_number

        self.players = players
        self.boards = self.init_boards()
        self.deck = Deck((self.boards[0].rect.w * 0.14, self.boards[0].rect.h * 0.14))
        self.last_turn = False
        self.game_over = False
        self.turn = 0
        self.columns_active_effects_used = [False] * 5

        self.active_board = self.boards[0]
        self.active_board.current_tile = self.deck.draw()
        self.active_board.set_position((self.screen_width // 2 - self.active_board.rect.w // 2,
                                        self.screen_height // 2 - self.active_board.rect.h // 2))
        self.inactive_boards = self.boards[1:]

        # now pygame part
        self.flip_button = Button('assets/buttons/flip_button.png', convert_alpha=True)
        self.flip_button = self.flip_button.resize(2)
        self.flip_button.set_position((self.screen_width // 2 - self.flip_button.rect.w // 2,
                                       self.screen_height * 0.95 - self.flip_button.rect.h))

        self.blit(self.flip_button, self.flip_button.rect.topleft)

    def add_players(self, players):
        self.players.extend(players)

    def init_boards(self):
        return [Board((self.screen_height * 2 // 3, self.screen_height * 2 // 3), self.board_number,
                      self.players[i], self.players)
                for i in range(self.number_players)]

    def update_game_state(self):
        if self.last_turn and self.turn % self.number_players == 0:
            pygame.event.post(pygame.event.Event(END_GAME))
            return

        self.blit(self.background, (0, 0))

        for i, board in enumerate(self.inactive_boards):
            if not board.minimised:
                x = self.screen_width // 4 if i % 2 == 0 else self.screen_width * 3 // 4
                x -= board.minimised_background_image.rect.w if i % 2 == 0 else 0
                y = self.screen_height // 3
                y += -board.minimised_background_image.rect.h * 0.6 if i < 2 else board.minimised_background_image.rect.h * 0.6
                board.set_position((x, y))
                board.minimise(self.background)
            else:
                x = self.screen_width // 4 if i % 2 == 0 else self.screen_width * 3 // 4
                x -= board.minimised_background_image.rect.w if i % 2 == 0 else 0
                y = self.screen_height // 3
                y += -board.minimised_background_image.rect.h * 0.6 if i < 2 else board.minimised_background_image.rect.h * 0.6
                board.set_position((x, y))
                board.fill_background(self.background)

            board.update()
            self.blit(board, board.rect.topleft)
            # blit the name of the player under the board
            font = pygame.font.Font('assets/fonts/ShinyCrystal.ttf', 40)
            text = font.render(board.board_manager.player.username, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.topleft = (board.rect.x + board.rect.w // 2 - text_rect.w // 2, board.rect.y + board.rect.h)
            self.blit(text, text_rect.topleft)

        if self.active_board.minimised:
            self.active_board.maximise()
            self.active_board.set_position((self.screen_width // 2 - self.active_board.rect.w // 2,
                                            self.screen_height // 2 - self.active_board.rect.h // 2))
        self.active_board.update()
        self.blit(self.active_board, self.active_board.rect.topleft)
        # blit the name of the player under the board
        font = pygame.font.Font('assets/fonts/ShinyCrystal.ttf', 70)
        text = font.render(self.active_board.board_manager.player.username, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (self.active_board.rect.x + self.active_board.rect.w // 2 - text_rect.w // 2,
                             self.active_board.rect.y + self.active_board.rect.h)
        self.blit(text, text_rect.topleft)

        if self.active_board.monkeying:
            for pos in self.active_board.flippable_tiles_pos:
                rect = self.active_board.columns_rects[pos[0]][pos[1] - self.active_board.board_manager.columns[pos[0]].gap_from_the_bottom]
                relative_rect = (rect.x + self.active_board.rect.x, rect.y + self.active_board.rect.y, rect.w, rect.h)
                pygame.draw.rect(self, (255, 0, 0), relative_rect, 3)

        self.blit(self.flip_button, self.flip_button.rect.topleft)

        pygame.display.flip()

    def event_handler(self, event):
        if event:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.flip_button.rect.collidepoint(event.pos) and not self.active_board.monkeying:
                    self.active_board.current_tile.flip()

            elif event.type == COLUMN_ACTIVE_EFFECT_USED:
                self.columns_active_effects_used[event.column_number] = True
                for board in self.boards:
                    board.board_manager.columns_active_effects_used[event.column_number] = True

            elif event.type == MONKEY_ACT:
                if event.tiles_pos:
                    self.active_board.flippable_tiles_pos = event.tiles_pos
                    self.active_board.monkeying = True
                else:
                    pygame.event.post(pygame.event.Event(END_TURN))

            elif event.type == PARROT_ACT:
                self.active_board.current_tile = self.deck.draw()

            elif event.type == BOARD_FINISHED:
                self.last_turn = True

            elif event.type == END_GAME and not self.game_over:
                self.game_over = True
                print("ending the game")
                print(self.boards)
                for board in self.boards:
                    print("oooooooo")
                    board.board_manager.apply_end_effects()

                pygame.event.post(pygame.event.Event(CHANGE_TO_END_GAME, players=self.players))

            elif event.type == END_TURN:
                self.active_board.board_manager.check_end()
                if self.turn % self.number_players == 0:
                    for player in self.players:
                        if player.map_possessor:
                            player.gold += 1
                            print("1 gold added to the map possessor:", player.username)
                self.turn += 1

                print(f"at the end of the turn {self.turn}:")
                for player in self.players:
                    print(f"-{player.username} has {player.gold} gold and is {'not ' if not player.map_possessor else ''}"
                          f"the map possessor")

                if self.inactive_boards:
                    active_board_n = self.turn % self.number_players
                    self.active_board = self.boards[active_board_n]
                    self.inactive_boards = self.boards[:active_board_n] + self.boards[active_board_n + 1:]
                self.active_board.current_tile = self.deck.draw()

            self.active_board.event_handler(event)

            self.update_game_state()
