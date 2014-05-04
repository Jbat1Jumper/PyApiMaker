from . import api


with api.context("auth"):

    @api.add()
    def login(user, password):
        pass

    @api.add()
    def register_user(user, password, profile_dict):
        pass

    @api.add()
    def delete_user(token):
        pass

    @api.add()
    def change_password(token, new_password):
        pass
