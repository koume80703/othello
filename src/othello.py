import numpy as np
from state import State
from mcts.node import Node
from mcts.mcts import MCTS

import time

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

    def list_flippable_stone(self, x, y, player):
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
                while(True):
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

    def list_placable_stone(self, player):
        placable = []

        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.RawBoard[y+1][x+1] != EMPTY:
                    continue
                if self.list_flippable_stone(x+1, y+1, player) == []:
                    continue
                else:
                    placable.append((x+1, y+1))

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


class Game(Board):
    DRAW = 0

    def __init__(self, turn=0, start_player=BLACK):
        super().__init__()
        self.player = start_player
        self.turn = turn
        self.winner = None
        self.was_passed = False
        self.set_order = []

        self.START_PLAYER = start_player

    def is_finished(self):
        return self.winner != None

    def list_placable_stone(self):
        return super().list_placable_stone(self.player)

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
        if super().set_stone(x, y, self.player):
            self.was_passed = False
            self.shift_player()            
            self.turn += 1
            self.set_order.append((self.player,x,y))
        else:
            return False

    def pass_moving(self):
        if self.was_passed:
            return self.finish_game()

        self.was_passed = True
        self.shift_player()
        self.set_order.append((0,-1,-1))

    def show_score(self):
        print("{}: {}".format("WHITE", self.stones[0]))
        print("{}: {}".format("BLACK", self.stones[1]))

        print("Winner: {}".format(self.get_color(self.winner)))
        
    def get_stone_num(self):
        white = 0
        black = 0
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.RawBoard[y+1][x+1] == WHITE:
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


def main():
    GAME_NUM = 20

    count_cycle = 0
    count_won = 0
    count_lose = 0
    count_draw = 0

    total_time = 0

    for _ in range(GAME_NUM):
        count_cycle += 1
        print("cycle: ",count_cycle)
        game = Game()
        state = State(game)
        while True:
            if state.is_done():
                state.game.show_board()
                state.game.show_score()
                if state.is_draw():
                    count_draw += 1
                    print("draw")
                elif state.is_lose():
                    count_lose += 1
                    print("lose")
                else:
                    count_won += 1
                    print("win")
                break
                        
            if state.legal_actions() == []:
                state = state.pass_moving()
                continue
            if state.is_first_player():
                root_node = Node(state, expand_base=70)

                start_time = time.time()
                MCTS.train(root_node=root_node, simulation=1000)            
                elapsed_time = time.time() - start_time
                print("elapsed time: {0:.2f}".format(elapsed_time) + "[sec]\n")
                action = MCTS().select_action(root_node)
                state = state.next(action)
            else:
                action = state.random_action()
                state = state.next(action)

    print()
    print("win: ", count_won)
    print("lose:", count_lose)
    print("draw:", count_draw)

    print("total time: {0:.2f}".format(total_time) + "[sec]")
    print("average elapsed time: {0:.2f}".format(total_time / GAME_NUM) + "[sec]")

if __name__ == "__main__":
    main()
