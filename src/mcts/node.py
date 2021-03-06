from __future__ import annotations

from typing import List

from mcts.util.argmax import argmax
from mcts.util.ucb1 import ucb1

import copy


class Node:
    def __init__(self, state, base_player, expand_base: int = 20) -> None:
        self.state = state
        self.w: float = 0
        self.n: int = 0
        self.expand_base: int = expand_base
        self.children: List[Node] = []

        self.base_player = base_player

    def evaluate(self) -> float:
        if self.state.is_done():
            value = -1 if self.state.is_lose() else 0
            self.w += value
            self.n += 1
            return value

        if self.children == []:
            value = Node.playout(
                copy.deepcopy(self.state), base_player=self.base_player
            )
            self.w += value
            self.n += 1

            if self.n == self.expand_base:
                self.expand()
            return value
        else:
            value = self.next_child_based_ucb().evaluate()
            self.w += value
            self.n += 1
            return value

    def expand(self) -> None:
        if self.state.legal_actions() == []:
            return
        self.children = [
            Node(self.state.next(action), self.base_player, self.expand_base)
            for action in self.state.legal_actions()
        ]

    def next_child_based_ucb(self) -> Node:
        for child in self.children:
            if child.n == 0:
                return child

        sn = sum([child.n for child in self.children])
        ucb1_values = [ucb1(sn, child.n, child.w) for child in self.children]

        return self.children[argmax(ucb1_values)]

    @classmethod
    def playout(cls, state, base_player) -> float:
        if state.is_done():
            if state.is_win(base_player):
                return 1
            elif state.is_lose(base_player):
                return -1
            else:
                return 0

        if state.legal_actions() == []:
            state = state.pass_moving()
            return Node.playout(state, base_player)
        else:
            return Node.playout(state.next(state.random_action()), base_player)
