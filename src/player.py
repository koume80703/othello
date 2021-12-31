from typing import Tuple
from mcts.node import Node
from mcts.mcts import MCTS


WHITE = -1
BLACK = 1


class Player:
    def __init__(self, name):
        self.name = name

    def mcts_action(self, state, expand_base=20, simulation=100) -> Tuple[int, int]:
        root_node = Node(state, self.name, expand_base=expand_base)
        MCTS.train(root_node=root_node, simulation=simulation)
        action = MCTS.select_action(root_node)
        return action

    def random_action(self, state):
        return state.random_action()
