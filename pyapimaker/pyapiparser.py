from ._util import smatch


class PyApiParser():

    def __init__(self, pool=None, only_names=False):
        self.pool = pool or [[[]]][0][0]
        self.only_names = only_names

    def split(self, cmd):
        if isinstance(cmd, list):
            return [c for c in cmd if c]
        else:
            return [c for c in cmd.split(" ") if c]

    def parse_sysargs_call(self):
        import sys
        args = sys.argv[1: len(sys.argv)]
        r = self.call(args)
        if r:
            print(r)

    def parse_sysargs_extended(self):
        import sys
        args = sys.argv[1: len(sys.argv)]
        r = self.parse_extended(args)
        if r:
            print(r)

    def parse_extended(self, cmd):
        cmdlets = self.split(cmd)
        if not cmdlets:
            return None
        action = cmdlets.pop(0)

        if smatch(action, "call|c"):
            return self.parse_call(cmdlets)
        elif smatch(action, "help|h"):
            return self.parse_help(cmdlets)
        elif smatch(action, "list|ls|l"):
            return self.list(cmdlets)

    def parse_call(self, cmd):
        try:
            cmdlets = self.split(cmd)
            if not cmdlets:
                return "must provide a function"
            kn = cmdlets.pop(0)
            for f in self.pool:
                if (self.only_names and f.name == kn)\
                        or (not self.only_names and f.key == kn):
                    if len(cmdlets) != len(f.args):
                        return "Error: {0} takes {1} arguments,"\
                               " but {2} was given".format(f.key, len(f.args),
                                                           len(cmdlets))
                    return f.call(*cmdlets)
            return "no function found"
        except Exception as e:
            return "Error: {}".format(repr(e))

    def parse_help(self, cmd):
        cmdlets = self.split(cmd)
        if not cmdlets:
            return self.extended_help()
        kn = cmdlets.pop(0)
        for f in self.pool:
            if (self.only_names and f.name == kn)\
                    or (not self.only_names and f.key == kn):
                return f.doc
        return "no function found"

    def extended_help(self):
        return "\n"\
            "Extended parse help - aviable commands:\n\n"\
            "    call|c <foo> [args] : call a function with given args\n"\
            "    help|h [foo] : shows this help or function doc if aviable\n"\
            "    list|l [context] [name] : list all functions and also can filter\n"

    def list(self, cmd):
        name, context = "*", "*"
        cmdlets = self.split(cmd)
        if cmdlets:
            context = cmdlets.pop(0)
        if cmdlets:
            name = cmdlets.pop(0)
        s = "\n"
        for f in self.pool:
            if smatch(f.name, name) and smatch(f.context, context):
                s += repr(f) + "\n"
        return s
