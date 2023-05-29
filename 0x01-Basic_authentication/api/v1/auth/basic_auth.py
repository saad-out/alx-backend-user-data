#!/usr/bin/env python3
""" Module of class Auth to manage the API authentication.
"""
import base64

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Class to manage the app authentication.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ Method to extract the base64 authorization header.
        """
        AUTH_SCHEME = "Basic "

        if authorization_header is None:
            return None
        try:
            assert type(authorization_header) == str
        except AssertionError:
            return None
        if not authorization_header.startswith(AUTH_SCHEME):
            return None

        return authorization_header[len(AUTH_SCHEME):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Method to decode the base64 authorization header.
        """
        if base64_authorization_header is None:
            return None
        try:
            assert type(base64_authorization_header) == str
        except AssertionError:
            return None

        try:
            byte_auth = bytes(base64_authorization_header, "utf-8")
            data = base64.b64decode(byte_auth)
        except Exception:
            return None
        return data.decode("utf-8")

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Method to extract the user credentials.
        """
        try:
            assert decoded_base64_authorization_header is not None
            assert type(decoded_base64_authorization_header) == str
            assert ":" in decoded_base64_authorization_header
        except AssertionError:
            return None, None

        return tuple(decoded_base64_authorization_header.split(":"))
