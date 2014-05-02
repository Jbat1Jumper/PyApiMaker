from flask import Flask, Blueprint, request, render_template_string, Response
from .json_response import GoodResponse, ErrorResponse
import os


class PyRpcServer():
    def __init__(self, name="PyRpcServer", ip="127.0.0.1", port=5000, debug=False):
        self.fapp = Flask(name)
        self.name = name
        self.ip = ip
        self.port = port
        self.debug = debug
        self.fapp.debug = self.debug
        if self.debug:
            self.fapp.config['PROPAGATE_EXCEPTIONS'] = True

    def run(self):
        print("Staring {s.name} server on {s.ip}:{s.port}".format(s=self))
        return self.fapp.run(self.ip, self.port)

    def add(self, bp):
        self.fapp.register_blueprint(bp.bp, url_prefix=bp.prefix)


class PyRpcBlueprint():
    def __init__(self, name=None, importName=__name__, prefix=None, action="call"):
        self.name = name
        self.importName = importName
        self.prefix = prefix
        self.foos = {}
        self.bp = Blueprint(self.name, self.importName)
        self.action = action
        self.actionFoo = self.getActionFromStr(self.action)
        self.bp.route('/<func>', methods=['POST', 'GET'])(self.actionFoo)

    def add(self, foos, onlyNames=False):
        for foo in foos:
            key = onlyNames and foo.name or foo.key
            self.foos[key] = foo

    def getActionFromStr(self, s):
        if s == "call":
            return self.rpcCall
        elif s == "fancyCall":
            return self.rpcFancyCall
        elif s == "help":
            return self.rpcHelp
        elif s == "fancyHelp":
            return self.rpcFancyHelp
        else:
            raise Exception("Invalid action")

    def rpcCall(self, func):
        try:
            f = self.foos[func]
            args = f.args[:]
            # TODO: Make the code below beautiful
            for arg in args:
                if not arg in request.values:
                    break
            else:
                kwargs = {}
                for arg in args:
                    kwargs[arg] = request.values.get(arg, None)
                retval = f.call(**kwargs)
                return GoodResponse(retval)
            for n in range(len(args)):
                if not "arg{}".format(n) in request.values:
                    break
            else:
                oargs = []
                for n in range(len(args)):
                    oargs.append(request.values.get("arg{}".format(n)))
                retval = f.call(*oargs)
                return GoodResponse(retval)
            return ErrorResponse(2, "Wrong parameters")
        except KeyError:
            return ErrorResponse(3, "Function '" + func + "' was not found")
        except Exception as e:
            return ErrorResponse(1, repr(e))

    def rpcFancyCall(self, func):
        return "<pre>{}</pre>".format(self.rpcCall(func))

    def rpcHelp(self, func):
        try:
            f = self.foos[func]
            return GoodResponse(f.doc)
        except KeyError:
            return ErrorResponse(3, "Function '" + func + "' was not found")
        except Exception as e:
            return ErrorResponse(1, repr(e))

    def rpcFancyHelp(self, func):
        return "<pre>{}</pre>".format(self.rpcHelp(func))


class PyRpcTerminal():
    def __init__(self, name=None, importName=__name__, prefix=None, encode=True):
        self.name = name
        self.importName = importName
        self.prefix = prefix
        self.bp = Blueprint(self.name, self.importName)
        self.action = None
        self.handler = None
        self.encode = encode
        self.bp.route('/')(self.terminalt)
        self.bp.route('/resources/<res>')(self.resourcest)
        self.bp.route('/handler', methods=['POST', 'GET'])(self.handleRequest)

    def terminalt(self):
        d = os.path.dirname(__file__)
        with open(os.path.join(d, "resources/terminal.html"), "r") as f:
            return render_template_string(f.read(), name=self.name, callurl="./handler")

    def resourcest(self, res):
        d = os.path.dirname(__file__)
        mimetypes = {
            ".css": "text/css",
            ".html": "text/html",
            ".js": "application/javascript",
        }
        with open(os.path.join(d, "resources/", res), "r") as f:
            m = mimetypes[(os.path.splitext(res)[1])]
            return Response(f.read(), mimetype=m)

    def handleRequest(self):
        if not self.handler:
            return ErrorResponse(4, "This therminal does not have a command handler")
        try:
            cmd = request.values.get("cmd", None)
            if not cmd:
                return ErrorResponse(5, "There is no 'cmd' in args")
            if self.encode:
                cmd = self.decode(cmd)
            r = self.handler(cmd)
            return GoodResponse(r)
        except Exception as e:
            return ErrorResponse(1, repr(e))

    def decode(self, s):
        return s  # TODO
