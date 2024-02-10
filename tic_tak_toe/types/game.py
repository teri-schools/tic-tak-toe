from tic_tak_toe.types import Board, Player, UndoMove
from tic_tak_toe.utils import clear_console



class Game:
    def __init__(self, *players):
        self.players = list(players)
        self.board = None
        self._current_player = None
        self._close: bool = True
        self.restart(False)

    def restart(self, change_badge: bool = True):
        if change_badge:
            for player in self.players:
                player.change_badge()
        self._current_player = self.players.index(self.get_player_by_badge("X"))
        self.board = Board()
        return self

    @property
    def current_player(self):
        return self.players[self._current_player]

    def next_player(self):
        self._current_player = (self._current_player + 1) % len(self.players)

    def get_player_by_badge(self, badge: str):
        for player in self.players:
            if player.badge == badge:
                return player

    def get_winner(self) -> Player:
        winner_badge = self.board.get_winner()
        if winner_badge is not None:
            return self.get_player_by_badge(winner_badge)

    def _play(self):
        while True:
            clear_console()
            self.board.draw_board()
            if win_player := self.get_winner():
                win_player.say_win_message()
                win_player.score += 1
                return win_player
            if self.board.is_full():
                print("It's a draw")
                return None
            # move player
            try:
                self.current_player.move(self.board)
                self.next_player()
            except UndoMove:
                self.undo_move()

    def undo_move(self):
        ...

    def play(self):
        self._close = False
        result = self._play()
        self._close = True
