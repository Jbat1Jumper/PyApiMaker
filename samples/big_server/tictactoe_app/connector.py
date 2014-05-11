from pyapimaker import PyRpcConnector


server = PyRpcConnector(url="localhost:17887/rpc", timeout=0.5)

s_login = server.bind_function("auth.login")
s_storage = server.bind_container("app_storage")
