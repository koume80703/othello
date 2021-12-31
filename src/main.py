from board import BLACK, WHITE
from player import Player
from game import Game
from state import State

START_PLAYER = BLACK


def main():
    GAME_NUM = 20

    count_cycle = 0
    count_won, count_lose, count_draw = 0, 0, 0

    total_time = 0

    player1 = Player(BLACK)
    player2 = Player(WHITE)

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
                action = player1.mcts_action(state)
                state = state.next(action)
            else:
                action = player2.mcts_action(state, expand_base=100, simulation=1000)
                state = state.next(action)

        state.game.board.show_board()
        state.game.show_score()
        if state.is_draw():
            count_draw += 1
        elif state.is_lose(START_PLAYER):
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
