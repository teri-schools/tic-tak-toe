from typing import List, Union

from tic_tak_toe.types import Badge, Board, UndoMove
from tic_tak_toe.utils import ConsoleSession


class Player:
    def __init__(self, name: str, badge: Badge, score: int = 0):
        self.name = name
        self.score = score
        self.badge = Badge(badge)

    def change_badge(self):
        self.badge = ~self.badge

    def move(self, board: Board):
        print(f"{self.name}'s turn: Select from 1 to {board.size ** 2} from the game board.")
        while True:
            char = input().strip()
            if char.lower() == "u":
                raise UndoMove()
            if not char.isdigit() or not 1 <= int(char) <= (board.size ** 2):
                print(f"Please enter a valid number between 1 and {(board.size ** 2)}.")
                continue
            if board.get_cell(int(char)) is None:
                return board.move(int(char), self.badge)
            print(f"There is no cell '{char}' on the field")

    def say_win_message(self):
        print(f"Player '{self.name}' has wins!")

    @classmethod
    def from_console(cls, badge: str = None, text: str = "What is your name?\n"):
        with ConsoleSession():
            name = input(text).strip()
            if not badge:
                badge = input("Select your badge: X or O\n").strip().lower()
                badge = Badge(badge)
            return cls(name=name, badge=badge)


class PCPlayer(Player):
    def __init__(self, badge: str):
        super().__init__("PC", badge, 0)

    def get_weight_combination(self, row: List[Union[Badge, int]]):
        is_self = row.count(self.badge)
        is_other = row.count(~self.badge)
        if is_self > 0 or is_other == 0:
            return 2 * is_self
        if is_self > 0 and is_other > 0:
            return 0
        if is_self == 0 and is_other > 0:
            return 2 * is_other
        return 1

    def get_best_position(self, board: Board):
        grid = []
        for x in range(board.size):
            row = []
            for y in range(board.size):
                cell = board.board[x][y]
                if cell is None:
                    row.append(0)
                else:
                    row.append(cell)
            grid.append(row)
        # Check rows
        for row in grid:
            for i in range(len(row)):
                if isinstance(row[i], int):
                    row[i] += self.get_weight_combination(row)
        # Check columns
        for col in range(board.size):
            colums = [row[col] for row in grid]
            for i in range(len(grid)):
                if isinstance(grid[i][col], int):
                    grid[i][col] += self.get_weight_combination(colums)
        # Check diagonals
        diagonal1 = [grid[i][i] for i in range(board.size)]
        for i in range(board.size):
            if isinstance(grid[i][i], int):
                grid[i][i] += self.get_weight_combination(diagonal1)

        diagonal2 = [grid[i][board.size - 1 - i] for i in range(board.size)]
        for i in range(board.size):
            if isinstance(grid[i][board.size - 1 - i], int):
                grid[i][board.size - 1 - i] += self.get_weight_combination(diagonal2)

        maxs_row = [max([cell for cell in row if isinstance(cell, int)] or [-1]) for row in grid]
        max_v = max(maxs_row)
        x = maxs_row.index(max_v)
        y = grid[x].index(max_v)
        return (x * board.size) + y + 1

    def move(self, board: Board):
        print(f"{self.name}'s turn:")
        num = self.get_best_position(board)
        return board.move(num, self.badge)

    def say_win_message(self):
        print("Player 'PC' has won!\n"
              "You is looking for a winner!")

    @classmethod
    def from_console(cls, badge: str = None):
        if not badge:
            badge = BadgeEnum.circle
        return cls(badge)
