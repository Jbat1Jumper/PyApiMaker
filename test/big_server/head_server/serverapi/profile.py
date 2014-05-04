from . import api


with api.context("profile"):

    @api.add()
    def create_profile(token, profile_dict):
        pass

    @api.add()
    def get_profile(token):
        pass

    @api.add()
    def update_profile(token, profile_dict):
        pass
