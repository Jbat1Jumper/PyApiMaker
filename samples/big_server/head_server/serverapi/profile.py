from pyapimaker import PyApiException
from json import loads, dumps
from . import api

from .auth import validate_token

# bad
from storage import storage

# Error codes of profile
#
# Field doesn't exist - 1101


with api.context("profile"):

    @api.add()
    def get_profile(token):
        """
        Returns the profile json dict of the user
        Args:
            token (str): The auth token of the user.
        Returns:
            str with the json dict of the profile
        Raises:
            Invalid token - 1004
        """
        u = validate_token(token)
        with storage.context("profiles") as st:
            p = st.get(u.username)
            return dumps(p)

    @api.add()
    def update_profile(token, profile_dict):
        """
        Receives a json dict with all fields
        and updates it into the actual profile
        Args:
            token (str): The auth token of the user.
        Returns:
            str with the json dict of the profile
        Raises:
            Invalid token - 1004
        """
        u = validate_token(token)
        with storage.context("profiles") as st:
            p = st.get(u.username)
            n_p = loads(profile_dict)
            p.update(n_p)
            st.put(u.username, p)
            return dumps(p)

    @api.add()
    def update_field(token, field, value):
        """
        Updates the given field of the profile dict
        Args:
            token (str): The auth token of the user.
            field (str): The name of the field to update.
            value (str): The string with the value to update.
        Returns:
            True if was updated.
        Raises:
            Invalid token - 1004
        """
        u = validate_token(token)
        with storage.context("profiles") as st:
            p = st.get(u.username)
            p[field] = str(value)
            st.put(u.username, p)
            return True

    @api.add()
    def get_field(token, field):
        """
        Returns the given field of the profile dict in json format.
        Args:
            token (str): The auth token of the user.
            field (str): The name of the field.
        Returns:
            str with the value.
        Raises:
            Field doesn't exist - 1101
            Invalid token - 1004
        """
        u = validate_token(token)
        with storage.context("profiles") as st:
            p = st.get(u.username)
            if not field in p:
                raise PyApiException(1101, "Field doesn't exist")
            return str(p[field])
