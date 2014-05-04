from flask import Flask, Blueprint, request, render_template_string, Response
from .json_response import GoodResponse, ErrorResponse
from zipfile import ZipFile
from .pyapiexception import PyApiException
import os
import io


class PyRpcServer():

    def __init__(self, name="PyRpcServer", ip="127.0.0.1", port=5000,
                 debug=False):
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

    def __init__(self, name=None, import_name=__name__, prefix=None,
                 action="call", encode=False, acao=None):
        self.name = name
        self.import_name = import_name
        if prefix == "/":
            prefix = None
        self.prefix = prefix
        self.foos = {}
        self.encode = encode
        self.bp = Blueprint(self.name, self.import_name)
        self.action = action
        self.acao = acao
        self.action_foo = self._get_action_from_str(self.action)
        self.bp.route('/<func>', methods=['POST', 'GET'])(self.action_foo)
        self.bp.route('/', methods=['POST', 'GET'])(self.ping_foo)

    def set_acao(self, response):
        response = Response(response, mimetype="application/json")
        if not self.acao:
            return response
        response.headers["Access-Control-Allow-Origin"] = self.acao
        return response

    def ping_foo(self):
        return self.set_acao(GoodResponse("connection ok"))

    def add(self, foos, only_names=False):
        for foo in foos:
            key = only_names and foo.name or foo.key
            self.foos[key] = foo

    def _get_action_from_str(self, s):
        if s == "call":
            return self.rpc_call
        elif s == "fancy_call":
            return self.rpc_fancy_call
        elif s == "help":
            return self.rpc_help
        elif s == "fancy_help":
            return self.rpc_fancy_help
        else:
            raise Exception("Invalid action")

    def rpc_call(self, func):
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
                return self.set_acao(GoodResponse(retval))
            for n in range(len(args)):
                if not "arg{}".format(n) in request.values:
                    break
            else:
                oargs = []
                for n in range(len(args)):
                    oargs.append(request.values.get("arg{}".format(n)))
                retval = f.call(*oargs)
                return self.set_acao(GoodResponse(retval))
            return self.set_acao(ErrorResponse(2, "Wrong parameters"))
        except KeyError:
            return self.set_acao(ErrorResponse(3, "Function '" + func + "' was not found"))
        except PyApiException as e:
            return self.set_acao(ErrorResponse(e.error_code, e.erro_desc))
        except Exception as e:
            return self.set_acao(ErrorResponse(1, repr(e)))

    def rpc_fancy_call(self, func):
        return "<pre>{}</pre>".format(self.rpc_call(func))
        # TODO: make it more fancy

    def rpc_help(self, func):
        try:
            f = self.foos[func]
            return self.set_acao(GoodResponse(f.doc))
        except KeyError:
            return self.set_acao(ErrorResponse(3, "Function '" + func + "' was not found"))
        except PyApiException as e:
            return self.set_acao(ErrorResponse(e.error_code, e.erro_desc))
        except Exception as e:
            return self.set_acao(ErrorResponse(1, repr(e)))

    def rpc_fancy_help(self, func):
        return "<pre>{}</pre>".format(self.rpc_help(func))
        # TODO: make it more fancy


class PyRpcTerminal():

    def __init__(self, name="PyRpcTerminal", import_name=__name__, prefix=None,
                 encode=True):
        self.name = name
        self.import_name = import_name
        if prefix == "/":
            prefix = None
        self.prefix = prefix
        self.bp = Blueprint(self.name, self.import_name)
        self.action = None
        self.handler = None
        self.encode = encode
        self.bp.route('/')(self.terminalt)
        self.bp.route('/resources/<res>')(self.resourcest)
        self.bp.route('/handler', methods=['POST', 'GET'])(self.handle_request)

    def terminalt(self):
        d = os.path.dirname(__file__)
        with ZipFile(os.path.join(d, "resources"), "r") as z:
            with z.open("terminal.html", "r") as f:
                f = io.TextIOWrapper(f)
                return render_template_string(f.read(), name=self.name,
                                              callurl="./handler")

    def resourcest(self, res):
        d = os.path.dirname(__file__)
        mimetypes = {
            ".css": "text/css",
            ".html": "text/html",
            ".js": "application/javascript",
        }
        with ZipFile(os.path.join(d, "resources"), "r") as z:
            with z.open(res, "r") as f:
                f = io.TextIOWrapper(f)
                m = mimetypes[(os.path.splitext(res)[1])]
                return Response(f.read(), mimetype=m)

    def handle_request(self):
        if not self.handler:
            return ErrorResponse(4, "This therminal does not have a "
                                    "command handler")
        try:
            cmd = request.values.get("cmd", None)
            if not cmd:
                return ErrorResponse(5, "There is no 'cmd' in args")
            if self.encode:
                cmd = self.decode(cmd)
            r = self.handler(cmd)
            return GoodResponse(r)
        except PyApiException as e:
            return ErrorResponse(e.error_code, e.erro_desc)
        except Exception as e:
            return ErrorResponse(1, repr(e))

    def decode(self, s):
        return s  # TODO
