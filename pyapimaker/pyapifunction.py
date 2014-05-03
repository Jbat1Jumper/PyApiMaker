
class PyApiFunction():

    def __init__(self, func):
        from inspect import getdoc
        self.func = func
        self.name = func.__name__
        self.context = "none"
        self.key = "%s.%s" % (self.context, self.name)
        self.args = self._getwrappedargspecs(func)
        self.doc = getdoc(func)

    def _getwrappedargspecs(self, foo):
        from inspect import getfullargspec
        args, _, _, _, _, _, _ = getfullargspec(foo)
        if hasattr(foo, "__wrapped__"):
            args.extend(self._getwrappedargspecs(foo.__wrapped__))
        return args

    def get_arg_names(self):
        return self.args[:]

    def call(self, *args, **kwargs):
        self.check_all_args_here(*args, **kwargs)
        return self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def check_all_args_here(self, *args, **kwargs):
        return True  # TODO

    def to_json(self):
        return {"context": self.context, "name": self.name, "args": self.args}

    def __repr__(self):
        args = ", ".join(self.args)
        return "<%s(%s)>" % (self.key, args)
