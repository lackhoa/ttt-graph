from Board import Board
from Board import Cell
from Tree import Node
from graphviz import Digraph

# Make a board
board = Board()
# Make a node (The root node)
root = Node(board)

# board1 = Board()
# board1.cells[0][1] = Cell.o
# node1 = Node(board1)

# board2 = Board()
# board2.cells[1][1] = Cell.o
# board2.cells[0][1] = Cell.x
# node2 = Node(board2)

# root.add_child(node1)
# node1.add_child(node2)

lvl = 2
for i in range(0, lvl):
    for node in root.get_nodes_lvl(i):
        node.explore()

# Try and clean up the bad routes:
clean_up = False
if clean_up:
    for i in range(lvl):
        for node in root.get_nodes_lvl(i):
            if node.is_bad:
                if node.parents:
                    for parent in node.parents:
                        parent.children.remove(node)

# Then print everything out:
gr = Digraph(name='graph', node_attr={'shape': 'plaintext'}, format="png")

for i in range(lvl):
    for node in root.get_nodes_lvl(i):
        gr.node(name=node.id, label=node.board.to_graph_viz())
        for child in node.children:
            gr.node(name=child.id, label=child.board.to_graph_viz())
            gr.edge(tail_name=node.id, head_name=child.id)

gr.render(filename='out/lvl2.gv'.format(lvl.__str__(), clean_up.__str__()))




