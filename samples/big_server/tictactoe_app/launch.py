from game import game 
from gameapi import game_api

from pyapimaker import PyApiParser


parser = PyApiParser(only_names=True)
quit = False

if __name__ == "__main__":

    print("Welcome to super boring tic tac toe")

    while not quit:
        cmd = input("tictactoe-{}> ".format(game.context))
        parser.pool = game_api.find_functions(context=game.context)

        resp = parser.parse_call(cmd)

        if resp == "no function found":
            resp = "what did you say"
        if resp:
            print(resp)

        if game.context is None:
            quit = True
