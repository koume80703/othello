from __future__ import annotations
from mcts.istate import IState
from mcts.util.argmax import argmax
from mcts.util.ucb1 import ucb1

import copy

class Node:
    def __init__(self, state: IState, expand_base: int = 20) -> None:
        self.state: IState = copy.deepcopy(state)
        self.w: int = 0
        self.n: int = 0
        self.expand_base: int = expand_base
        self.children: Optional[List[Node]] = None

    def evaluate(self) -> float:
        """現在のノードの評価値を計算して更新する。"""
        
        if self.state.is_done():
            value = -1 if self.state.is_lose() else 0
            self.w += value
            self.n += 1
            return value

        if self.children is None:            
            v = Node.playout(copy.deepcopy(self.state))            
            self.w += v
            self.n += 1

            if self.n == self.expand_base:
                self.expand()
            return v
        else:
            v = self.next_child_based_ucb().evaluate()
            self.w += v
            self.n += 1
            return v

    def expand(self) -> None:
        if self.state.legal_actions() == []:
            return
        self.children = [Node(self.state.next(action), self.expand_base) for action in self.state.legal_actions()]        

    def next_child_based_ucb(self) -> Node:
        for child in self.children:
            if child.n == 0:
                return child

        sn = sum([child.n for child in self.children])
        ucb1_values = [ucb1(sn, child.n, child.w) for child in self.children]
        
        return self.children[argmax(ucb1_values)]

    @classmethod
    def playout(cls, state: IState) -> float:
        if state.is_done():
            if state.is_win():
                return 1
            elif state.is_lose():
                return -1
            else:
                return 0

        if state.legal_actions() == []:
            state = state.pass_moving()
            return Node.playout(state)
        else:
            return Node.playout(state.next(state.random_action()))