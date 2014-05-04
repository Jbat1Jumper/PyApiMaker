import shelve
from pyapimaker import PyApi

storage = PyApi()


users = shelve.open("users.db")

with storage.context("users"):
    @storage.add()
    def get(name):
        return users.get(name, None)

    @storage.add()
    def put(name, user):
        users[name] = user
        users.sync()

    @storage.add()
    def rem(name):
        del users[name]
        users.sync()


profiles = shelve.open("profiles.db")

with storage.context("profiles"):
    @storage.add()
    def get(name):
        return profiles.get(name, {})

    @storage.add()
    def put(name, profile_dict):
        profiles[name] = profile_dict
        profiles.sync()

    @storage.add()
    def rem(name):
        del profiles[name]
        profiles.sync()

# . . .


def close_everything():
    print("closing databases")
    users.close()
    profiles.close()
