from pyapimaker import PyApiException
from . import api

# bad imports
from storage import storage
from user import User, decode_token


# Auth exception numbers:
#
# User doesn't exist - 1001
# User already exist - 1002
# Wrong password - 1003
# Invalid token - 1004


def validate_token(token):
    """parses the token
    if its a valid token return the User object
    otherwise raises an Invalid token exception
    """
    with storage.context("users") as st:
        try:
            user, token_date = decode_token(token)
        except Exception:
            raise PyApiException(1004, "Invalid token")
        u = st.get(user)
        if not u or not u.is_token_valid(token):
            raise PyApiException(1004, "Invalid token")
        return u


with api.context("auth"):

    @api.add()
    def login(user, password):
        """
        Login with the selected user and get the auth_token.
        Args:
            user (str):  The username to login.
            password (str):  The password of the user.
        Returns:
            str with the auth_token
        Raises:
            User doesn't exist - 1001
            Wrong password - 1003
        """
        with storage.context("users") as st:
            u = st.get(user)
            if not u:
                raise PyApiException(1001, "User doesn't exist")
            if u.password != password:
                raise PyApiException(1003, "Wrong password")
            token = u.create_token()
            st.put(user, u)
            return token

    @api.add()
    def register_user(user, password):
        """
        Create a new user if doesn't already exist.
        Args:
            user (str):  The username for the new user.
            password (str):  The password for the user.
        Returns:
            str with the auth_token
        Raises:
            User already exists - 1002
        """
        with storage.context("users") as st:
            if st.get(user):
                raise PyApiException(1002, "User already exist")
            u = User(user, password)
            token = u.create_token()
            st.put(user, u)
            return token

    @api.add()
    def delete_user(token):
        """
        Delete the user and his profile
        Args:
            token (str):  The auth token of the user.
        Returns:
            True if deleted
        Raises:
            Invalid token - 1004
        """
        u = validate_token(token)
        rem_foos = storage.find_functions(name="rem",
                                          context="users|profiles|vault")
        for rem in rem_foos:
            try:
                rem(u.username)
            except Exception:
                continue
        return True

    @api.add()
    def change_password(token, new_password):
        """
        Change the password of the user given by token.
        Args:
            token (str):  The auth token of the user.
            new_password (str): The new password.
        Returns:
            True if successful
        Raises:
            Invalid token - 1004
        """
        with storage.context("users") as st:
            u = validate_token(token)
            st.put(u.username, u)
            return True
