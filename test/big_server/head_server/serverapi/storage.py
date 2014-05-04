from . import api


with api.context("storage"):

    @api.add()
    def put(token, key, value):
        pass

    @api.add()
    def rem(token, key):
        pass

    @api.add()
    def get(token, key):
        pass

    @api.add()
    def list(token, key):
        pass
