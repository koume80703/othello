import time

from board import BLACK, WHITE
from game import Game
from player import Player
from state import State
from output_log import output_log

START_PLAYER = BLACK


def main():
    GAME_NUM = 20

    count_play = 0
    count_won, count_lose, count_draw = 0, 0, 0

    total_time1 = 0
    total_time2 = 0

    player1 = Player(BLACK)
    player2 = Player(WHITE)

    for _ in range(GAME_NUM):
        count_play += 1
        output_log("<play: {}".format(count_play))

        game = Game()
        state = State(game)
        while not state.is_done():
            if state.legal_actions() == []:
                state = state.pass_moving()
                continue
            if state.is_first_player():
                start = time.time()
                action = player1.mcts_action(state)
                elapsed = time.time() - start
                output_log("player1's elapsed time: {:.2f}".format(elapsed))
                total_time1 += elapsed
                state = state.next(action)
            else:
                start = time.time()
                action = player2.mcts_action(state, expand_base=100, simulation=1000)
                elapsed = time.time() - start
                output_log("player2's elapsed time: {:.2f}".format(elapsed))
                total_time2 += elapsed
                state = state.next(action)

        state.game.board.show_board()
        state.game.show_score()
        if state.is_draw():
            count_draw += 1
        elif state.is_lose(START_PLAYER):
            count_lose += 1
        else:
            count_won += 1

    output_log(
        "win: {0}, lose: {1}, draw: {2}".format(count_won, count_lose, count_draw)
    )
    output_log("total time of player1:         : {:.2f} [sec]".format(total_time1))
    output_log(
        "average elapsed time of player1: {:.2f} [sec]".format(total_time1 / GAME_NUM)
    )
    output_log("total time of player2          : {:.2f} [sec]".format(total_time2))
    output_log(
        "average elapsed time of player2: {:.2f} [sec]".format(total_time2 / GAME_NUM)
    )


if __name__ == "__main__":
    main()
