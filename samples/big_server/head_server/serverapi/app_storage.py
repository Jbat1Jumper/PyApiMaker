from pyapimaker import PyApiException
from . import api
from .auth import validate_token
import json

# bad
from storage import storage

# Error codes of app storage
#
# App storage doesn't exsit - 1201
# Key doesn't exist - 1202


with api.context("app_storage"):

    @api.add()
    def get(token, app_name):
        """
        Returns the json string of the given user app storage.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage to return.
        Returns:
            json dict of all the storage.
        Raises:
            Invalid token - 1004
            App storage doesn't exsit - 1201
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                raise PyApiException(1201, "App storage doesn't exist")
            return us[app_name]

    @api.add()
    def put(token, app_name, app_storage_dict):
        """
        Puts the app_storage_dict as the app_name storage of
        the given user.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name with which save the storage.
            app_storage_dict (str): The json of the storage dict to save.
        Returns:
            True if ok.
        Raises:
            Invalid token - 1004
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            us[app_name] = json.loads(app_storage_dict)
            st.put(u.username, us)
            return True

    @api.add()
    def update(token, app_name, app_storage_dict):
        """
        Updates the keys and values of app storage with the
        provided dict for the given user.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage to update.
            app_storage_dict (str): A json string with a dict with
                the values to update
        Returns:
            str with the updated storage.
        Raises:
            Invalid token - 1004
            App storage doesn't exsit - 1201
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                raise PyApiException(1201, "App storage doesn't exist")
            us[app_name].update(json.loads(app_storage_dict))
            st.put(u.username, us)
            return us[app_name]

    @api.add()
    def create_if_not_exist(token, app_name, app_storage_dict):
        """
        Updates the keys and values of app storage with the
        provided dict for the given user without override.
        It only creates new keys if they doesn't exist.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage to update.
            app_storage_dict (str): A json string with a dict with
                the values to update
        Returns:
            str with the updated storage.
        Raises:
            Invalid token - 1004
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                us[app_name] = {}
            d = json.loads(app_storage_dict)
            d.update(us[app_name])
            us[app_name] = d
            st.put(u.username, us)
            return us[app_name]

    @api.add()
    def rem(token, app_name):
        """
        Deletes the given app storage of the given user.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage to delete.
        Returns:
            True if was deleted.
        Raises:
            Invalid token - 1004
            App storage doesn't exsit - 1201
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                raise PyApiException(1201, "App storage doesn't exist")
            del us[app_name]
            st.put(u.username, us)
            return True

    @api.add()
    def get_from(token, app_name, key):
        """
        Gets the value of the specified key in the given user storage.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage.
            key (str): The key of what to retrive from the storage.
        Returns:
            the retrived object.
        Raises:
            Invalid token - 1004
            App storage doesn't exsit - 1201
            Key doesn't exist - 1202
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                raise PyApiException(1201, "App storage doesn't exist")
            if not key in us[app_name]:
                raise PyApiException(1202, "Key doesn't exist")
            return us[app_name][key]

    @api.add()
    def put_to(token, app_name, key, value):
        """
        Sets the value of the given key in the given user storage.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage.
            key (str): The key where you want to store tha value.
            value (str): The value to set.
        Returns:
            True if was stored.
        Raises:
            Invalid token - 1004
            App storage doesn't exsit - 1201
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                raise PyApiException(1201, "App storage doesn't exist")
            us[app_name][key] = value
            st.put(u.username, us)
            return True

    @api.add()
    def rem_from(token, app_name, key):
        """
        Removes the value from the given user app storage.
        Args:
            token (str): The auth token of the user.
            app_name (str): The name of the storage.
            key (str): The key of what you want to remove.
        Returns:
            True if it was deleted.
        Raises:
            Invalid token - 1004
            App storage doesn't exsit - 1201
            Key doesn't exist - 1202
        """
        u = validate_token(token)
        with storage.context("app_storage") as st:
            us = st.get(u.username)
            if not app_name in us:
                raise PyApiException(1201, "App storage doesn't exist")
            if not key in us[app_name]:
                raise PyApiException(1202, "Key doesn't exist")
            del us[app_name][key]
            st.put(u.username, us)
            return True
