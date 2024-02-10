import os
from typing import List

def draw_table(table: List[List[str]]):
    collum_count = max(map(len, table))
    row_count = len(table)
    rows = []
    for row in table:
        row: List[str]
        rows.append("|".join(map(
            lambda x: str(x).center(3),
            row
        )))
    sep = "-"*((collum_count * 4) - 1)
    print(f"\n{sep}\n".join(rows))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class ConsoleSession:
    def __enter__(self):
        pass
        # clear_console()

    def __exit__(self, exc_type, exc_val, exc_tb):
        clear_console()
