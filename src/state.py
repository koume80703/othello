from __future__ import annotations
from random import choice
from mcts.istate import IState
from typing import List, Optional
import copy

class State(IState):
    def __init__(self, game: Game):
        self.game = copy.deepcopy(game)

    def next(self, action: (int, int)) -> State:
        n_state = State(self.game)
        n_state.game.set_stone(*action)
        return n_state
    
    def pass_moving(self) -> State:
        n_state = State(self.game)
        n_state.game.pass_moving()
        return n_state
    
    def legal_actions(self) -> List[(int, int)]:
        return self.game.list_placable_stone()
    
    def random_action(self) -> (int,int):
        return choice(self.legal_actions())

    def winner(self) -> int:
        return self.game.winner

    def is_win(self) -> bool:
        return True if self.game.START_PLAYER == self.winner() else False

    def is_lose(self) -> bool:
        return True if self.game.START_PLAYER == -self.winner() else False

    def is_draw(self) -> bool:
        return True if self.winner() == self.game.DRAW else False

    def is_done(self) -> bool:
        return self.game.is_finished()
    
    def is_first_player(self) -> bool:
        return self.game.START_PLAYER == self.game.player