
class PyApiContext():
    def __init__(self, api, context):
        self.__my_api = api
        self.__my_context = context

    def __enter__(self):
        self.__my_api.enter_context(self.__my_context)
        for foo in self.__my_api.find_functions(context=self.__my_context):
            self.__dict__[foo.name] = foo
        return self

    def __exit__(self, ty, val, trace):
        self.__my_api.exit_context(self.__my_context)

    def __repr__(self):
        c = self.__my_context
        f = ""
        for foo in self.__my_api.find_functions(context=self.__my_context):
            f += "    " + repr(foo) + "\n"
        return "<context: {0}\n  functions:\n{1}>".format(c, f)
