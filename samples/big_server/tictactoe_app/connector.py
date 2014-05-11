from pyapimaker import PyRpcConnector


server = PyRpcConnector(url="localhost:17887/rpc")

s_login = server.bind_function("auth.login")
s_storage = server.bind_container("app_storage")
