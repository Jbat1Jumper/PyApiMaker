from pyapimaker import PyApi
from connector import server, s_login, s_storage
from game import game
import logic
from random import randint
from textwrap import dedent
import json

game_api = PyApi()


def get_clean_storage():
    return {"win": 0, "lost": 0, "draw": 0, "surrender": 0, "played": 0}


def get_from_storage(key):
    resp = s_storage.get_from(game.usertoken, game.storage, key)
    if resp.had_errors:
        return None
    return json.loads(str(resp.content))


def storage_increment(key):
    if server.is_online():
        s = get_from_storage(key)
        put_to_storage(key, s + 1)


def put_to_storage(key, value):
    resp = s_storage.put_to(game.usertoken, game.storage, key, value)
    if resp.had_errors:
        return False
    return True


def get_storage():
    resp = s_storage.get(game.usertoken, game.storage)
    if resp.had_errors:
        return None
    return resp.content


def create_storage(usertoken):
    cs = json.dumps(get_clean_storage())
    resp = s_storage.create_if_not_exist(usertoken, game.storage, cs)


with game_api.context("login"):
    @game_api.add()
    def login(username, password):
        if not server.is_online():
            return "server is not online now, retry later"
        response = s_login(username, password)
        if response.had_errors:
            return "login failed, " + response.error_desc
        usertoken = response.content
        game.username = username
        game.usertoken = usertoken
        game.context = "lobby"
        create_storage(usertoken)
        return "logged successful"

    @game_api.add(name="help")
    def _help():
        return dedent("""\
            you can use:
            login <username> <password> = to login
            exit = to exit""")

    @game_api.add(name="exit", context="lobby")
    @game_api.add(name="exit")
    def _exit():
        game.context = None
        return "goodbye"


with game_api.context("lobby"):
    @game_api.add()
    def logout():
        game.clean()
        return "logged out"

    @game_api.add()
    def stats():
        if not server.is_online():
            return "server is not online"
        st = get_storage()
        return dedent("""\
            played a total of {played} games:
                won {win} of them
                lost {lost} of them, with honor
                draw {draw} of them
                and miserably surrendered {surrender} games""").format(**st)

    @game_api.add()
    def play():
        game.token = randint(0, 100) > 50 and "X" or "O"
        game.context = "play"
        game.clean_board()
        storage_increment("played")
        print("starting match with {}".format(game.token))
        if game.token == "O":
            print("ia is playing")
            ix, iy = logic.hard_ia_turn(game.board, None, None, "X")
            if not ix is None:
                game.board[ix][iy] = game.token == "X" and "O" or "X"
            print("done")
        return "now its your turn"

    @game_api.add(name="help")
    def _help():
        return dedent("""\
            you can use:
            play = to start a new game
            stats = to show your game stats
            show = to show the game board
            exit = to logout and exit""")


with game_api.context("play"):
    @game_api.add(context="lobby")
    @game_api.add()
    def show():
        li = []
        for c in game.board:
            for r in c:
                li.append(r)
        return dedent("""\
            board:
                        1     2     3
                    a   {}  |  {}  |  {}
                      -----|-----------
                    b   {}  |  {}  |  {}
                      -----------|-----
                    c   {}  |  {}  |  {}
            """).format(*li)

    @game_api.add()
    def surrender():
        game.context = "lobby"
        storage_increment("surrender")
        return "boooooo"

    @game_api.add()
    def put(token, x, y):
        if token.upper() != game.token:
            return "you cant, you are {}".format(game.token)

        x = x.replace("a", "1")
        x = x.replace("b", "2")
        x = x.replace("c", "3")
        x, y = int(x)-1, int(y)-1
        b = game.board
        try:
            if b[x][y] != "_":
                return "its already occupied"
            b[x][y] = game.token
            print("done")
        except Exception:
            return "are you mad?"

        if logic.who_wins(b) != "_" or logic.is_full(b):
            game_over()
            return ""
        print("ia is playing")
        ix, iy = logic.dumb_ia_turn(game.board, x, y, "X")
        if not ix is None:
            b[ix][iy] = game.token == "X" and "O" or "X"
        print("done")
        if logic.who_wins(b) != "_" or logic.is_full(b):
            game_over()
            return ""
        return "now its your turn"

    def game_over():
        print("game over")
        winner = logic.who_wins(game.board)
        if winner == "_":
            storage_increment("draw")
            print("nobody win")
            print("its a draw")
        elif winner == game.token:
            storage_increment("win")
            print("{} wins".format(winner))
            print("you win")
        else:
            storage_increment("lost")
            print("{} wins".format(winner))
            print("you lose")
        game.context = "lobby"

    @game_api.add()
    def help():
        return dedent("""\
            you can use:
            show = shows the game board
            surrender = coward
            put <X|O> <row> <column> = mark the given position""")
