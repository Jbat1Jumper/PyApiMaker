from pyapimaker import PyRpcConnector


if __name__ == "__main__":

    c = PyRpcConnector(url="localhost:17887/rpc")

    if not c.is_online():
        print("RPC server is not online")
        exit()
    else:
        print("RPC server is on")

    foo_a = c.bind_function("foo_a")

    print("calling function foo_a:")
    r = foo_a()
    print(r.had_errors)
    print(r.error_code)
    print(r.error_desc)
    print(r.content)

    with c.bind_container() as web:

        print("calling function foo_b:")
        r = web.foo_b(li=["a", "b", "c"], num=23)
        print(r.had_errors)
        print(r.error_code)
        print(r.error_desc)
        print(r.content)
