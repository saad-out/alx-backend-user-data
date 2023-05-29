#!/usr/bin/env python3
""" Module of class Auth to manage the API authentication.
"""
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
