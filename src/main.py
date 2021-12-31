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
        while not state.is_done():
            if state.legal_actions() == []:
                state = state.pass_moving()
                continue
            if state.is_first_player():
                root_node = Node(state, expand_base=20)

                start_time = time.time()
                MCTS.train(root_node=root_node, simulation=100)
                elapsed_time = time.time() - start_time
                total_time += elapsed_time
                print(f"elapsed time: {elapsed_time:.2f}")
                action = MCTS().select_action(root_node)
                state = state.next(action)
            else:
                action = state.random_action()
                state = state.next(action)

        state.game.board.show_board()
        state.game.show_score()
        if state.is_draw():
            count_draw += 1
        elif state.is_lose():
            count_lose += 1
        else:
            count_won += 1

    print()
    print(f"win:  {count_won}")
    print(f"lose: {count_lose}")
    print(f"draw: {count_draw}")

    print(f"total time: {total_time:.2f}[sec]")
    print(f"average elapsed time: {total_time / GAME_NUM:.2f} [sec]")


if __name__ == "__main__":
    main()
