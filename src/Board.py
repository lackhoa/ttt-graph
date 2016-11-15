from enum import Enum


class Cell(Enum):
    vacant = " - "
    o = "O"
    x = "X"

"""
This is a TicTacToe board
The "O" player always goes first
The matrix writing order is row first, column later
"""
class Board:
    def __init__(self):
        # Create an initial board with 3 rows and 3 columns all set to vacant
        self.cells = [[Cell.vacant for x in range(3)] for y in range(3)]

    def set_cells(self, new_cells):
        self.cells = new_cells

    # Return the "Console" look of the board:
    def __str__(self):
        temp = self.cells

        return (temp[0][0].value + temp[0][1].value + temp[0][2].value + "\n" +
                temp[1][0].value + temp[1][1].value + temp[1][2].value + "\n" +
                temp[2][0].value + temp[2][1].value + temp[2][2].value)

    # Return the graphviz syntax:
    def to_graph_viz(self):
        tmp = self.cells
        # Setting the border color:
        if (self.turn() == Cell.o):
            border_color = "red"
        else:
            border_color = "green"

        # Setting the fill color:
        fill_color = "white"
        style = ""

        if self.did_ox_win(Cell.o):
            fill_color = "green"
        elif self.did_ox_win(Cell.x):
            fill_color = "red"
        elif self.is_draw():
            fill_color = "blue:white"
            style = "radial"
        elif self.close_to_win(Cell.o) and self.close_to_win(Cell.x):
            fill_color = "yellow:white"
            style = "radial"
        elif self.close_to_win(Cell.o):
            fill_color = "green:white"
            style = "radial"
        elif self.close_to_win(Cell.x):
            fill_color = "red:white"
            style = "radial"

        return ('''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" COLOR="{9}" BGCOLOR="{10}" style="{11}">
          <TR>
            <TD>{0}</TD>
            <TD>{1}</TD>
            <TD>{2}</TD>
          </TR>
          <TR>
            <TD>{3}</TD>
            <TD>{4}</TD>
            <TD>{5}</TD>
          </TR>
          <TR>
            <TD>{6}</TD>
            <TD>{7}</TD>
            <TD>{8}</TD>
          </TR>
        </TABLE>>''').format(tmp[0][0].value, tmp[0][1].value, tmp[0][2].value,
                             tmp[1][0].value, tmp[1][1].value, tmp[1][2].value,
                             tmp[2][0].value, tmp[2][1].value, tmp[2][2].value,
                             border_color, fill_color, style)

    # Return the exact same board
    def clone(self):
        clone = Board()
        clone.set_cells(self.cells.copy())
        return clone

    # Compare this to another board
    def is_equal(self, another_board):
        tmp1 = self.cells
        tmp2 = another_board.cells

        for x in range(3):
            for y in range(3):
                if tmp1[x][y] != tmp2[x][y]:
                    return False

        return True

    # See if this board is equivalent to another board
    def is_equivalent(self, another_board):
        # Check direction
        if self.is_equal(another_board):
            return True
        # Check the rotations:
        for r in self.__get_symmetries():
            if r.is_equal(another_board):
                return True

        return False

    # Get all the possible rearrangements of the board (all 3 of them)
    def __get_symmetries(self):
        result = []

        # First rotation clockwise:
        cw1 = self.__get_rotation_cw()
        cw2 = cw1.__get_rotation_cw()
        cw3 = cw2.__get_rotation_cw()

        # Second: reflection:
        p = self.__get_reflection()
        pcw1 = p.__get_rotation_cw()
        pcw2 = pcw1.__get_rotation_cw()
        pcw3 = pcw2.__get_rotation_cw()

        result.append(cw1)
        result.append(cw2)
        result.append(cw3)
        result.append(p)
        result.append(pcw1)
        result.append(pcw2)
        result.append(pcw3)

        return result

    # return the rotation like the third dimension:
    def __get_reflection(self):
        tmp1 = self.cells
        tmp2 = [[Cell.vacant for x in range(3)] for y in range(3)]

        tmp2[0][0] = tmp1[0][2]
        tmp2[0][1] = tmp1[0][1]
        tmp2[0][2] = tmp1[0][0]
        tmp2[1][0] = tmp1[1][2]
        tmp2[1][1] = tmp1[1][1]
        tmp2[1][2] = tmp1[1][0]
        tmp2[2][0] = tmp1[2][2]
        tmp2[2][1] = tmp1[2][1]
        tmp2[2][2] = tmp1[2][0]

        result = Board()
        result.set_cells(tmp2)
        return result

    # return the board rotated clockwise:
    def __get_rotation_cw(self):
        tmp1 = self.cells
        tmp2 = [[Cell.vacant for x in range(3)] for y in range(3)]

        tmp2[0][0] = tmp1[2][0]
        tmp2[0][1] = tmp1[1][0]
        tmp2[0][2] = tmp1[0][0]
        tmp2[1][0] = tmp1[2][1]
        tmp2[1][1] = tmp1[1][1]
        tmp2[1][2] = tmp1[0][1]
        tmp2[2][0] = tmp1[2][2]
        tmp2[2][1] = tmp1[1][2]
        tmp2[2][2] = tmp1[0][2]

        result = Board()
        result.set_cells(tmp2)
        return result

    # Return the current active player (the player that will play next move)
    def turn(self):
        tmp = self.cells
        # Count the number of vacant cell
        vacant_num = 0
        for x in range(3):
            for y in range(3):
                if tmp[x][y] == Cell.vacant:
                    vacant_num += 1

        # Then determine the result:
        if vacant_num % 2 == 0:
            return Cell.x
        else:
            return Cell.o

    # This function test if a player may end the game in the next move:
    # cell (Cell): indicates the player
    def close_to_win(self, cell):
        for line in self.get_all_lines():
            if line.count(cell) == 2 and line.count(Cell.vacant) == 1:
                return True

        return False

    def __is_line_close_to_win(self, line, cell):
        if line.count(cell) == 2 and line.count(Cell.vacant) == 1:
            return True

        return False

    # cell_type will win the game if he can:
    def win(self, cell_type):
        if self.__is_line_close_to_win(self.top_row, cell_type):
            self.top_row = [cell_type for cell in self.top_row]
            return
        if self.__is_line_close_to_win(self.middle_row, cell_type):
            self.middle_row = [cell_type for cell in self.middle_row]
            return
        if self.__is_line_close_to_win(self.bottom_row, cell_type):
            self.bottom_row = [cell_type for cell in self.bottom_row]
            return
        if self.__is_line_close_to_win(self.left_column, cell_type):
            self.left_column = [cell_type for cell in self.left_column]
            return
        if self.__is_line_close_to_win(self.middle_column, cell_type):
            self.middle_column = [cell_type for cell in self.middle_column]
            return
        if self.__is_line_close_to_win(self.right_column, cell_type):
            self.right_column = [cell_type for cell in self.right_column]
            return
        if self.__is_line_close_to_win(self.lr_cross, cell_type):
            self.lr_cross = [cell_type for cell in self.lr_cross]
            return
        if self.__is_line_close_to_win(self.rl_cross, cell_type):
            self.rl_cross = [cell_type for cell in self.rl_cross]
            return

    # Block (one of the) obvious winning move(s) of cell_type
    def block(self, cell_type):
        if cell_type == Cell.x:
            opp = Cell.o
        else:
            opp = Cell.x

        if self.__is_line_close_to_win(self.top_row, cell_type):
            self.top_row = [opp if cell == Cell.vacant else cell_type for cell in self.top_row]
            return

        if self.__is_line_close_to_win(self.middle_row, cell_type):
            self.middle_row = [opp if cell == Cell.vacant else cell_type for cell in self.middle_row]
            return

        if self.__is_line_close_to_win(self.bottom_row, cell_type):
            self.bottom_row = [opp if cell == Cell.vacant else cell_type for cell in self.bottom_row]
            return

        if self.__is_line_close_to_win(self.left_column, cell_type):
            self.left_column = [opp if cell == Cell.vacant else cell_type for cell in self.left_column]
            return

        if self.__is_line_close_to_win(self.middle_column, cell_type):
            self.middle_column = [opp if cell == Cell.vacant else cell_type for cell in self.middle_column]
            return

        if self.__is_line_close_to_win(self.right_column, cell_type):
            self.right_column = [opp if cell == Cell.vacant else cell_type for cell in self.right_column]
            return

        if self.__is_line_close_to_win(self.lr_cross, cell_type):
            self.lr_cross = [opp if cell == Cell.vacant else cell_type for cell in self.lr_cross]
            return

        if self.__is_line_close_to_win(self.rl_cross, cell_type):
            self.rl_cross = [opp if cell == Cell.vacant else cell_type for cell in self.rl_cross]
            return

    # This function test if a row or column can be the win row/column:
    def __can_still_win(self, line):
        if Cell.o not in line:
            return True
        if Cell.x not in line:
            return True
        return False

    # Test if the game is a draw:
    def is_draw(self):
        temp = self.cells

        for line in self.get_all_lines():
            if self.__can_still_win(line):
                return False

        return True

    # Test if someone is the winner
    # Provide the cell type in "cell" parameter
    def did_ox_win(self, cell):
        for line in self.get_all_lines():
            if all(c == cell for c in line):
                return True

        # If none are true then:
        return False

    # A bunch of getters and setters and properties:
    def get_top_row(self):
        temp = self.cells
        return [temp[0][0], temp[0][1], temp[0][2]]

    def set_top_row(self, x):
        temp = self.cells
        temp[0][0], temp[0][1], temp[0][2] = x[0], x[1], x[2]
    top_row = property(get_top_row, set_top_row)

    def get_middle_row(self):
        temp = self.cells
        return [temp[1][0], temp[1][1], temp[1][2]]

    def set_middle_row(self, x):
        temp = self.cells
        temp[1][0], temp[1][1], temp[1][2] = x[0], x[1], x[2]
    middle_row = property(get_middle_row, set_middle_row)

    def get_left_column(self):
        temp = self.cells
        return [temp[0][0], temp[1][0], temp[2][0]]

    def set_left_column(self, x):
        temp = self.cells
        temp[0][0], temp[1][0], temp[2][0] = x[0], x[1], x[2]
    left_column = property(get_left_column, set_left_column)

    def get_middle_column(self):
        temp = self.cells
        return [temp[0][1], temp[1][1], temp[2][1]]

    def set_middle_column(self, x):
        temp = self.cells
        temp[0][1], temp[1][1], temp[2][1] = x[0], x[1], x[2]

    middle_column = property(get_middle_column, set_middle_column)

    def get_right_column(self):
        temp = self.cells
        return [temp[0][2], temp[1][2], temp[2][2]]

    def set_right_column(self, x):
        temp = self.cells
        temp[0][2], temp[1][2], temp[2][2] = x[0], x[1], x[2]

    right_column = property(get_right_column, set_right_column)

    def get_bottom_row(self):
        temp = self.cells
        return [temp[2][0], temp[2][1], temp[2][2]]

    def set_bottom_row(self, x):
        temp = self.cells
        temp[2][0], temp[2][1], temp[2][2] = x[0], x[1], x[2]

    bottom_row = property(get_bottom_row, set_bottom_row)

    # The left to right cross:
    def get_lr_cross(self):
        temp = self.cells
        return [temp[0][0], temp[1][1], temp[2][2]]

    def set_lr_cross(self, x):
        temp = self.cells
        temp[0][0], temp[1][1], temp[2][2] = x[0], x[1], x[2]

    lr_cross = property(get_lr_cross, set_lr_cross)

    # The right to left cross:
    def get_rl_cross(self):
        temp = self.cells
        return [temp[0][2], temp[1][1], temp[2][0]]

    def set_rl_cross(self, x):
        temp = self.cells
        temp[0][2], temp[1][1], temp[2][0] = x[0], x[1], x[2]

    rl_cross = property(get_rl_cross, set_rl_cross)

    # Return all lines:
    def get_all_lines(self):
        return [self.top_row, self.middle_row, self.bottom_row, self.left_column,
                self.middle_column, self.right_column, self.lr_cross, self.rl_cross]
