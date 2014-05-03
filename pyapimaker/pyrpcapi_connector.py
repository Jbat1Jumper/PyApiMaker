from urllib import request, parse
from .json_response import RemoteResponse


class PyRpcConnector():

    def __init__(self, url=None, encode=False, method="POST"):
        self.url = url
        self.encode = encode
        self.method = method

    def is_online(self):
        try:
            url = parse.urljoin("http://mysticalserver", "//" + self.url + "/")
            # print(url)
            r = request.urlopen(url)
            if r.status != 200:
                js = '{"content": none,"error_code": %s,"error_desc": "%s",'\
                     '"had_errors": true}' % (str(r.status), r.reason)
            js = r.read().decode()
            rr = RemoteResponse(js)
            if rr.content == "connection ok":
                return True
        except Exception:
            pass
        return False

    def bind_container(self, context=None):
        return PyRpcContainter(self.url, self.method, context, self.encode)

    def bind_function(self, name):
        return PyRpcFunction(self.url, self.method, name, self.encode)


class PyRpcFunction():

    def __init__(self, url, method, name, encode=False):
        self.url = url
        self.name = name
        self.method = method

    def __call__(self, *args, **kwargs):
        data = {}
        for n, arg in enumerate(args):
            data["arg"+str(n)] = str(arg)
        for k, v in kwargs.items():
            data[k] = v

        resp = self.url_call(data)
        return RemoteResponse(resp)

    def url_call(self, data):
        try:
            data = parse.urlencode(data)
            url = parse.urljoin("http://", "//" + self.url + "/")
            url = parse.urljoin(url, self.name)

            if self.method == "POST":
                r = request.urlopen(url, data.encode())
            elif self.method == "GET":
                r = request.urlopen(url + ("?%" % data))
            else:
                raise Exception("Method %s not allowed" % self.method)

            if r.status != 200:
                return '{"content": none,"error_code": %s,"error_desc": "%s",'\
                       '"had_errors": true}' % (str(r.status), r.reason)
            return r.read().decode()

        except Exception as e:
            return '{"content": none,"error_code": 9,"error_desc": "%s",'\
                   '"had_errors": true}' % repr(e)


class PyRpcContainter():

    def __init__(self, url, method, context, encode=False):
        self.url = url
        self.method = method
        self.context = context
        self.encode = encode

    def __getattr__(self, k):
        if self.context:
            k = ".".join([self.context, k])
        return PyRpcFunction(self.url, self.method, k, self.encode)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass
