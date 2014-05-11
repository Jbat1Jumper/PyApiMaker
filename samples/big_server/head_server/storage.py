import shelve
from pyapimaker import PyApi
from config import config
storage = PyApi()

db_dir = config.get("db_dir", ".")

users = shelve.open(db_dir + "/users.db")

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


profiles = shelve.open(db_dir + "/profiles.db")

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


app_storage = shelve.open(db_dir + "/app_storage.db")

with storage.context("app_storage"):
    @storage.add()
    def get(user):
        return app_storage.get(user, {})

    @storage.add()
    def put(user, storage_dict):
        app_storage[user] = storage_dict
        app_storage.sync()

    @storage.add()
    def rem(user):
        del app_storage[user]
        app_storage.sync()

# . . .


def close_everything():
    print("DEBUG: closing databases")
    users.close()
    profiles.close()
    app_storage.close()
