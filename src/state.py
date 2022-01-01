from __future__ import annotations

from game import Game

import copy
from random import choice
from typing import List, Tuple, Optional


class State:
    def __init__(self, game: Game):
        self.game = copy.deepcopy(game)

    def next(self, action: Tuple[int, int]) -> State:
        n_state = State(self.game)
        n_state.game.set_stone(*action)
        return n_state

    def pass_moving(self) -> State:
        n_state = State(self.game)
        n_state.game.pass_moving()
        return n_state

    def legal_actions(self) -> List[Tuple[int, int]]:
        return self.game.list_placable_stone()

    def random_action(self) -> Tuple[int, int]:
        return choice(self.legal_actions())

    def winner(self) -> Optional[int]:
        return self.game.winner

    def is_win(self, base_player) -> bool:
        winner = self.winner()
        if winner is None:
            return False
        return True if winner == base_player else False

    def is_lose(self, base_player) -> bool:
        winner = self.winner()
        if winner is None:
            return False
        return True if winner == -base_player else False

    def is_draw(self) -> bool:
        return True if self.winner() == self.game.DRAW else False

    def is_done(self) -> bool:
        return self.game.is_finished()

    def is_first_player(self) -> bool:
        return self.game.START_PLAYER == self.game.player
