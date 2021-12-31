from board import Board
from typing import List, Tuple

WHITE = -1
BLACK = 1


class Game:
    DRAW = 0

    def __init__(self, turn=0, start_player=BLACK):
        self.board = Board()
        self.player = start_player
        self.turn = turn
        self.winner = None
        self.was_passed = False
        self.set_order = []

        self.START_PLAYER = start_player

    def is_finished(self):
        return self.winner is not None

    def list_placable_stone(self) -> List[Tuple[int, int]]:
        return self.board.list_placable_stone(self.player)

    def get_color(self, player):
        if player == WHITE:
            return "WHITE"
        if player == BLACK:
            return "BLACK"

        return "DRAW"

    def get_current_player(self):
        return self.player

    def get_next_player(self):
        return WHITE if self.player == BLACK else BLACK

    def shift_player(self):
        self.player = self.get_next_player()

    def set_stone(self, x, y):
        if self.board.set_stone(x, y, self.player):
            self.was_passed = False
            self.shift_player()
            self.turn += 1
            self.set_order.append((self.player, x, y))
        else:
            return False

    def pass_moving(self):
        if self.was_passed:
            return self.finish_game()

        self.was_passed = True
        self.shift_player()
        self.set_order.append((0, -1, -1))

    def show_score(self):
        print("{}: {}".format("WHITE", self.stones[0]))
        print("{}: {}".format("BLACK", self.stones[1]))

        print("Winner: {}".format(self.get_color(self.winner)))

    def get_stone_num(self):
        white = 0
        black = 0
        for x in range(self.board.BOARD_SIZE):
            for y in range(self.board.BOARD_SIZE):
                if self.board.RawBoard[y + 1][x + 1] == WHITE:
                    white += 1
                else:
                    black += 1

        return [white, black]

    def finish_game(self):
        self.stones = self.get_stone_num()
        white = self.stones[0]
        black = self.stones[1]

        if white < black:
            self.winner = BLACK
        elif black < white:
            self.winner = WHITE
        else:
            self.winner = self.DRAW
