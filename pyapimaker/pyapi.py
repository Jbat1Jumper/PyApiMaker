from .pyapicontext import PyApiContext
from .pyapifunction import PyApiFunction
from ._util import smatch


class PyApi():
    def __init__(self):
        self._context = []
        self._functions = {}

    def context(self, contextName=None):
        context = contextName or self.getActualContextName()
        return PyApiContext(self, context)

    def getActualContextName(self):
        if not self._context:
            return "none"
        else:
            return self._context[-1]

    def add(self, name=None, context=None):
        def foo(func):
            pam = PyApiFunction(func)
            pam.name = name or pam.name
            pam.context = context or self.getActualContextName()
            pam.key = "%s.%s" % (str(pam.context), str(pam.name))
            self._functions[pam.key] = pam
            return pam  # before it was the original func
        return foo

    def findFunctions(self, name="*", context=None):
        results = []
        context = context or self.getActualContextName()
        for foo in self._functions.values():
            if smatch(foo.name, name) and smatch(foo.context, context):
                results.append(foo)
        return results

    def getFunction(self, name, context=None):
        context = context or self.getActualContextName()
        key = "%s.%s" % (str(context), str(name))
        if key in self._functions:
            return self._functions[key]
        return None

    def enterContext(self, contextName):
        self._context.append(contextName)

    def exitContext(self, contextName=None):
        if self._context:  # if not last
            self._context.pop(-1)  # just pop last

    def discoverDirectory(self, directory):
        pass
