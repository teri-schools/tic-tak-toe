from typing import List, Optional, Tuple
from tic_tak_toe.utils import draw_table


class Badge(str):
    @property
    def dagger(self):
        """ "X" """
        return Badge("X")

    @property
    def circle(self):
        """ "O" """
        return Badge("O")

    def __new__(cls, badge: str):
        if badge.upper() == "X":
            badge = "X"
        else:
            badge = "O"
        return str.__new__(cls, badge)

    def __invert__(self):
        return Badge("X" if self == "O" else "O")


class Board:
    board: List[List[Optional[Badge]]]

    def __init__(self, size: int = 3):
        self.size = size
        self.board = [[None for i in range(size)] for j in range(size)]

    def get_position(self, num: int) -> Tuple[int, int]:
        num -= 1
        return num // self.size, num % self.size

    def get_winner(self) -> Badge:
        # Check rows
        for row in self.board:
            if all(row) and len(set(row)) == 1:
                return row[0]
        # Check columns
        for col in range(self.size):
            colums = [row[col] for row in self.board]
            if all(colums) and len(set(colums)) == 1:
                return self.board[0][col]
        # Check diagonals
        diagonal1 = [self.board[i][i] for i in range(min(len(self.board), len(self.board[0])))]
        if all(diagonal1) and len(set(diagonal1)) == 1:
            return diagonal1[-1]
        diagonal2 = [self.board[i][len(self.board[0]) - 1 - i] for i in range(min(len(self.board), len(self.board[0])))]
        if all(diagonal2) and len(set(diagonal2)) == 1:
            return diagonal2[-1]

    def get_cell(self, num: int) -> Optional[Badge]:
        x, y = self.get_position(num)
        return self.board[x][y]

    def set_cell(self, num: int, badge: Badge):
        x, y = self.get_position(num)
        self.board[x][y] = badge

    def draw_board(self):
        i = 0
        table = []
        for row in self.board:
            table_row = []
            for cell in row:
                i += 1
                if cell is None:
                    cell = i
                table_row.append(cell)
            table.append(table_row)
        draw_table(table)

    def is_full(self):
        return all([all(row) for row in self.board])
