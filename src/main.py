from state import State
from mcts.node import Node
from mcts.mcts import MCTS
from game import Game

import time


def main():
    GAME_NUM = 20

    count_cycle = 0
    count_won = 0
    count_lose = 0
    count_draw = 0

    total_time = 0

    for _ in range(GAME_NUM):
        count_cycle += 1
        print("cycle: ", count_cycle)
        game = Game()
        state = State(game)
        while True:
            if state.is_done():
                state.game.board.show_board()
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
