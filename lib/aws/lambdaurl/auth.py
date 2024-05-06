#!/usr/bin/env python3

"""
# 設定
app = LambdaURL()
auth = Authorization(app, TOKEN_PASSWORD, SESSION_PASSWORD)
id = auth.require_session()
"""

from re import search
from json import loads, dumps
from time import time
from base64 import b64decode, b64encode
from hashlib import sha256
from traceback import format_exc
from .lambda_url import LambdaURL
from urllib.parse import quote, unquote
from .bottle_router import HTTPError


class AuthSession:
    def __init__(self, app: LambdaURL, session_password: str) -> None:
        self.__session_password = session_password
        self.__payload: dict = None
        self.jwt = JWT()
        self.app = app

    def issue(self, d: dict):
        token = self.jwt.encode(d, self.__session_password)
        self.app.set_cookie(
            f"token={token}; max-age=315360000; Path=/; SameSite=None; Secure; HttpOnly;"
        )

    def __getitem__(self, key: str):
        if self.__payload is None:
            try:
                for cookie in self.app.cookies:
                    m = search("(?<=^token=)[^;]+(?=(;|$))", cookie.strip())
                    if m:
                        token = m.group()
                self.__payload = self.jwt.decode(token, self.__session_password)
            except Exception as e:
                print(format_exc())
                raise HTTPError(401, f"無効なセッションです: {format_exc()}")
        return self.__payload[key]


class AuthToken:
    def __init__(self, app: LambdaURL, token_password: str, expiration=30 * 60) -> None:
        self.__token_password = token_password
        self.__expiration = expiration
        self.__payload: dict = None
        self.jwt = JWT()
        self.app = app

    def __getitem__(self, key: str):
        if self.__payload is None:
            try:
                value = self.app.event["headers"]["authorization"].split(" ")[1]
                self.__payload = self.jwt.decode(value, self.__token_password)
                if self.__payload["iat"] + self.__expiration < time():
                    raise TimeoutError
            except Exception as e:
                print(format_exc())
                raise HTTPError(401, f"無効なトークンです: {value}")
        return self.__payload[key]


class JWT:
    def encode(self, d: dict, passwd: str):
        b64 = b64encode(dumps(d).encode()).decode()
        return quote(b64 + "." + self.__hash(b64 + passwd), safe="")

    def decode(self, token: str, passwd: str):
        [b64, hash] = unquote(token).split(".")
        assert hash == self.__hash(b64 + passwd)
        return loads(b64decode(b64))

    def __hash(self, text: str):
        return b64encode(sha256(text.encode()).digest()).decode()
