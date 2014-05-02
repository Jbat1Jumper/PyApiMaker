
class PyApiContext():
    def __init__(self, api, context):
        self.__myApi = api
        self.__myContext = context

    def __enter__(self):
        self.__myApi.enterContext(self.__myContext)
        for foo in self.__myApi.findFunctions(context=self.__myContext):
            self.__dict__[foo.name] = foo
        return self

    def __exit__(self, ty, val, trace):
        self.__myApi.exitContext(self.__myContext)

    def __repr__(self):
        c = self.__myContext
        f = ""
        for foo in self.__myApi.findFunctions(context=self.__myContext):
            f += "    " + repr(foo) + "\n"
        return "<context: {0}\n  functions:\n{1}>".format(c, f)
