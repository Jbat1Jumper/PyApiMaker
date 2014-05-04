from pyapimaker import PyRpcConnector


if __name__ == "__main__":

    print()
    c = PyRpcConnector(url="localhost:17887/rpc")

    if not c.is_online():
        print("RPC server is not online")
        exit()
    else:
        print("RPC server is on")

    foo_a = c.bind_function("foo_a")

    print()
    print("calling function foo_a:")
    r = foo_a()
    print("had errors: %s" % str(r.had_errors))
    print("error code: %s" % str(r.error_code))
    print("error desc: %s" % str(r.error_desc))
    print("content: %s" % str(r.content))

    with c.bind_container() as web:

        print()
        print("calling function foo_b:")
        r = web.foo_b(li=["a", "b", "c"], num=23)
        print("had errors: %s" % str(r.had_errors))
        print("error code: %s" % str(r.error_code))
        print("error desc: %s" % str(r.error_desc))
        print("content: %s" % str(r.content))
