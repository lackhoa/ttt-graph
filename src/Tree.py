from Board import Board
from Board import Cell
import copy

"""
Nodes are the game boards that represent scenarios that can happen in Tree

Attributes:
    Nodes must have board
    Beside the root, all nodes have parent(s) (a node)
    Nodes can have a list of children (that are nodes)
    Each node have a level number, root is lvl 0, its children are lvl 1, 2, 3 and so on...
"""


class Node:
    def __init__(self, board):
        # The Game Board that the node contains:
        self.board = board
        self.lvl = 0
        self.children = []
        self.parents = []
        self.id = str(0)

    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)
        child.lvl = self.lvl + 1
        if child.id == str(0):
            child.id = str(int(self.id) * 10 + self.children.__len__())

    # Get nodes of a specified level
    def get_nodes_lvl(self, lvl):
        root = self.__get_root()
        working_list = [root]

        for _ in range(lvl):
            temp = []
            for n in working_list:
                temp.extend(n.children)
            working_list = temp

        return set(working_list)

    def __get_root(self):
        result = None

        if not self.parents:
            return self
        else:
            working_node = self
            lvl = self.lvl
            while lvl != 0:
                working_node = working_node.parents[0]
                lvl = working_node.lvl

            return working_node

    # add possibilities to the node, return those possibilities
    # Now with the ability to pick the best move
    def explore(self):
        board = self.board
        cells = self.board.cells

        # If the game was over then don't do anything:
        draw = False
        o_won = False
        x_won = False
        # Must have at least 6 pieces:
        if self.lvl >= 6:
            draw = board.is_draw()
            x_won = board.did_ox_win(Cell.x)
        # Must have at least 5 pieces:
        if self.lvl >= 5:
            o_won = board.did_ox_win(Cell.o)

        if o_won or x_won or draw:
            return  # Don't do anything

        # See if it's "O" turn or "X" turn
        active_player = board.turn()

        # Traverse through the possibilities of the game:
        if active_player == Cell.o:
            opponent = Cell.x
        else:
            opponent = Cell.o
        # Test if someone is close to winning the game
        if board.close_to_win(active_player):
            # Then we will win the game:
            clone = copy.deepcopy(board)
            clone.win(active_player)
            scenarios = [clone]

        elif board.close_to_win(opponent):
            # We must stop the opponent immediately
            clone = copy.deepcopy(board)
            clone.block(opponent)
            scenarios = [clone]

        else:
            # Regular scenario:
            scenarios = []
            for x in range(3):
                for y in range(3):
                    # Ignore if the cell is occupied
                    if cells[x][y] != Cell.vacant:
                        continue

                    # If the cell is vacant, we're in business:
                    clone = copy.deepcopy(board)
                    clone.cells[x][y] = active_player
                    scenarios.append(clone)

        # Then we remove the symmetrical scenarios:
        final = [scenarios[0]]

        for s in scenarios:
            conflict = False
            for f in final:
                if s.is_equivalent(f):
                    conflict = True  # Oops! We already added that
                    break
            if not conflict:
                final.append(s)

        # And add the children to the node and we're done:
        # But wait! We must remove the cases that conflict with other cases as well
        same_lvl_nodes = self.get_nodes_lvl(self.lvl + 1)
        for f in final:
            conflict = False
            for same_lvl_node in same_lvl_nodes:
                if f.is_equivalent(same_lvl_node.board):
                    conflict = True
                    self.add_child(same_lvl_node)
                    break
            if not conflict:
                child = Node(f)
                self.add_child(child)

    @property
    def is_bad(self):
        if self.children:
            # o's turn: If all children is bad, then the node is bad
            # x's turn: If one children is bad, then the node is bad
            if self.board.turn() == Cell.o:
                bad_children = True
                for child in self.children:
                    if not child.is_bad:
                        bad_children = False

            else:
                bad_children = False
                for child in self.children:
                    if child.is_bad:
                        bad_children = True
                        break
        else:
            bad_children = False

        if self.board.did_ox_win(Cell.x) or bad_children:
            return True
        return False
