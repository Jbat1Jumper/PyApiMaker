from pyapimaker import PyRpcServer, PyRpcBlueprint
from pyapimaker import PyRpcTerminal, PyApiParser

from serverapi import api

all_api_funcs = api.find_functions(name="*", context="*")


from config import config

server = PyRpcServer(port=17887, debug=config["debug_enabled"])

# share all api in http://localhost:17887/rpc/
bp = PyRpcBlueprint(name="api", prefix="/rpc")
bp.add(all_api_funcs)
server.add(bp)

# create a parser for all api
parser = PyApiParser()
parser.pool = all_api_funcs

# show a terminal for all api in http://localhost:17887/term
tbp = PyRpcTerminal(name="", prefix="/")
tbp.handler = parser.parse_extended
server.add(tbp)


if __name__ == "__main__":
    # just run the server
    server.run()

    from storage import close_everything
    close_everything()
