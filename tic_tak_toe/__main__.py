import sys, os

from tic_tak_toe.types import Player, Game, PCPlayer
from tic_tak_toe.utils import ConsoleSession, clear_console

from pickle import dump, load

SAVE_PATH = "tic_tak_toe.pkl"

class Program:
    def __init__(self):
        clear_console()
        self.player1 = Player.from_console()
        self.last_game = None

    def main(self):
        try:
            print("Welcome to Tic-Tac-Toe")
            while True:
                self.menu()
        except KeyboardInterrupt:
            with open(SAVE_PATH, "wb") as fp:
                dump(self, fp)
            print("Close Tic Tac Toe!")

    def menu(self):
        if self.last_game is None:
            self.last_game = self.select_game()
        self.last_game.play()
        print("Do you want to play again? (y/n)")
        while 1:
            answer = input().strip().lower()
            if answer == "y":
                self.last_game.restart()
                break
            elif answer == "n":
                self.last_game = None
                break
            else:
                print("Invalid input")

    def select_game(self):
        with ConsoleSession():
            print("Select a game mode.\n"
                  "Write the number '1' for playing with the computer or '2' if playing with a friend: ")
            while True:
                game_mode = input().strip()
                if game_mode == "1":
                    return Game(
                        self.player1,
                        PCPlayer(~self.player1.badge)
                    )
                elif game_mode == "2":
                    return Game(
                        self.player1,
                        Player.from_console(~self.player1.badge)
                    )
                else:
                    print("Wrong input")


if __name__ == "__main__":
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "rb") as fp:
            program = load(fp)
    else:
        program = Program()
    program.main()
