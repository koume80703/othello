import numpy as np

from typing import List, Tuple

EMPTY = 0
WHITE = -1
BLACK = 1
WALL = 2


class Board:
    BOARD_SIZE = 8

    def __init__(self):
        self.RawBoard = np.zeros((self.BOARD_SIZE + 2, self.BOARD_SIZE + 2), dtype=int)

        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[self.BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, self.BOARD_SIZE + 1] = WALL

        self.RawBoard[4, 4] = WHITE
        self.RawBoard[5, 5] = WHITE
        self.RawBoard[4, 5] = BLACK
        self.RawBoard[5, 4] = BLACK

    def set_stone(self, x, y, player):
        if self.RawBoard[y][x] != EMPTY:
            return False

        flippable = self.list_flippable_stone(x, y, player)
        if flippable == []:
            return False

        self.RawBoard[y][x] = player
        for x, y in flippable:
            self.RawBoard[y][x] = -self.RawBoard[y][x]

        return True

    def list_flippable_stone(self, x, y, player) -> List[Tuple[int, int]]:
        PREV = -1
        NEXT = 1
        DIRECTION = [PREV, 0, NEXT]
        flippable = []

        for dx in DIRECTION:
            for dy in DIRECTION:
                if dx == 0 and dy == 0:
                    continue
                tmp = []
                depth = 0
                while True:
                    depth += 1

                    rx = x + (dx * depth)
                    ry = y + (dy * depth)

                    board_type = self.RawBoard[ry][rx]

                    if board_type == WALL or board_type == EMPTY:
                        break
                    else:
                        if board_type == player:
                            if tmp != []:
                                flippable.extend(tmp)
                            break
                        else:
                            tmp.append((rx, ry))

        return flippable

    def list_placable_stone(self, player) -> List[Tuple[int, int]]:
        placable = []

        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.RawBoard[y + 1][x + 1] != EMPTY:
                    continue
                if self.list_flippable_stone(x + 1, y + 1, player) == []:
                    continue
                else:
                    placable.append((x + 1, y + 1))

        return placable

    def show_board(self):
        print("--" * 20)
        for i in self.RawBoard:
            for j in i:
                if j == WHITE:
                    print("w", end=" ")
                elif j == BLACK:
                    print("b", end=" ")
                elif j == EMPTY:
                    print("*", end=" ")
                else:
                    print(".", end=" ")
            print("\n", end="")
        print("--" * 20)

    def get_board_state(self):
        return self.RawBoard
