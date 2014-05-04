from pyapimaker import PyApi
from pyapimaker import PyRpcServer, PyRpcBlueprint
from ast import literal_eval

api = PyApi()

storage = {}


@api.add()
def get_server_time():
    from time import gmtime, strftime
    return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())


@api.add()
def get_random_text():
    from random import randint
    n = randint(10, 20)
    s = ""
    for ne in range(n):
        le = randint(3, 10)
        for lee in range(le):
            s += chr(randint(97, 122))
        s += " "
    s += "eof."
    return s


@api.add()
def get_server_title():
    return "Hiper mega test server 2000"


if __name__ == "__main__":

    s = PyRpcServer(port=16319)

    bp = PyRpcBlueprint(name="web", prefix="/rpc", acao="*")

    bp.add(api.find_functions(), only_names=True)

    s.add(bp)

    s.run()
