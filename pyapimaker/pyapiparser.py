from ._util import smatch


class PyApiParser():
    def __init__(self, pool=None, onlyNames=False):
        self.pool = pool or [[[]]][0][0]
        self.onlyNames = onlyNames

    def split(self, cmd):
        if isinstance(cmd, list):
            return [c for c in cmd if c]
        else:
            return [c for c in cmd.split(" ") if c]

    def parseSysargsCall(self):
        import sys
        args = sys.argv[1: len(sys.argv)]
        r = self.call(args)
        if r:
            print(r)

    def parseSysargsExtended(self):
        import sys
        args = sys.argv[1: len(sys.argv)]
        r = self.parseExtended(args)
        if r:
            print(r)


    def parseExtended(self, cmd):
        cmdlets = self.split(cmd)
        if not cmdlets:
            return None
        action = cmdlets.pop(0)

        if smatch(action, "call|c"):
            return self.call(cmdlets)
        elif smatch(action, "help|h"):
            return self.help(cmdlets)
        elif smatch(action, "list|ls|l"):
            return self.list(cmdlets)

    def call(self, cmd):
        cmdlets = self.split(cmd)
        if not cmdlets:
            return "must provide a function"
        kn = cmdlets.pop(0)
        for f in self.pool:
            if (self.onlyNames and f.name == kn)\
                    or (not self.onlyNames and f.key == kn):
                if len(cmdlets) != len(f.args):
                    return "Error: {0} takes {1} arguments,"\
                           " but {2} was given".format(f.key, len(f.args),
                                                       len(cmdlets))
                return f.call(*cmdlets)
        return "no function found"

    def help(self, cmd):
        cmdlets = self.split(cmd)
        if not cmdlets:
            return self.extendedHelp()
        kn = cmdlets.pop(0)
        for f in self.pool:
            if (self.onlyNames and f.name == kn)\
                    or (not self.onlyNames and f.key == kn):
                return f.doc
        return "no function found"

    def extendedHelp(self):
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
