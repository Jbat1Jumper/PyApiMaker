from pyapimaker import PyApi
from pyapimaker import PyRpcServer, PyRpcBlueprint


myapi = PyApi()


@myapi.add()
def foo_a():
    print("foo_a is doing thing on serverside")
    return("things done")


@myapi.add()
def foo_b(li, num):
    print("foo_b is doing something on serverside")
    return [s + str(num) for s in li]


if __name__ == "__main__":

    s = PyRpcServer(port=17887)

    bp = PyRpcBlueprint(name="web", prefix="/rpc")

    bp.add(myapi.find_functions(), only_names=True)

    s.add(bp)

    s.run()
