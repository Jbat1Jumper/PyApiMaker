from .pyapicontext import PyApiContext
from .pyapifunction import PyApiFunction
from ._util import smatch


class PyApi():

    def __init__(self):
        self._context = []
        self._functions = {}

    def context(self, context_name=None):
        context = context_name or self.get_actual_context_name()
        return PyApiContext(self, context)

    def get_actual_context_name(self):
        if not self._context:
            return "none"
        else:
            return self._context[-1]

    def add(self, name=None, context=None):
        def foo(func):
            if hasattr(func, "func"):
                func = func.func
            pam = PyApiFunction(func)
            pam.name = name or pam.name
            pam.context = context or self.get_actual_context_name()
            pam.key = "%s.%s" % (str(pam.context), str(pam.name))
            self._functions[pam.key] = pam
            return pam  # before it was the original func
        return foo

    def find_functions(self, name="*", context=None):
        results = []
        context = context or self.get_actual_context_name()
        for foo in self._functions.values():
            if smatch(foo.name, name) and smatch(foo.context, context):
                results.append(foo)
        return results

    def get_function(self, name, context=None):
        context = context or self.get_actual_context_name()
        key = "%s.%s" % (str(context), str(name))
        if key in self._functions:
            return self._functions[key]
        return None

    def enter_context(self, context_name):
        self._context.append(context_name)

    def exit_context(self, context_name=None):
        if self._context:  # if not last
            self._context.pop(-1)  # just pop last

    def discover_directory(self, directory):
        pass
