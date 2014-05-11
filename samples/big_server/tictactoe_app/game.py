
class Game():

    def __init__(self):
        self.clean()

    def clean(self):
        self.context = "login"
        self.username = None
        self.usertoken = None
        self.storage = "TICTACTOE"
        self.token = "X"
        self.clean_board()

    def clean_board(self):
        self.board = []
        for n in range(3):
            self.board.append([])
            for m in range(3):
                self.board[n].append("_")

game = Game()


from gameapi import game_api
