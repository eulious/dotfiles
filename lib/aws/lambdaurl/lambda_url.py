#!/usr/bin/env python3

"""
# 設定
app = LambdaURL()

def lambda_handler(event, _):
    return app.request(event)

@app.post("/test/<id:int>")
def test()
    return {"status": "ok"}
"""

from json import dumps, loads
from base64 import b64decode
from traceback import format_exc
from .bottle_router import HTTPError, Router


class LambdaURL:
    def __init__(self, prefix="", origin="*"):
        self.event = {}
        self.cookies = []
        self.query_params = {}
        self.body = {}
        self.__router = Router()
        self.__set_cookie = ""
        self.__prefix = prefix
        self.__origin = origin

    def get(self, url: str):
        return self.__add(url, "GET")

    def post(self, url: str):
        return self.__add(url, "POST")

    def put(self, url: str):
        return self.__add(url, "PUT")

    def delete(self, url: str):
        return self.__add(url, "DELETE")

    def __add(self, url: str, method: str):
        def _wrapper(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            print(self.__prefix + url, method, func)
            self.__router.add(self.__prefix + url, method, func)
            return wrapper

        return _wrapper

    def lambda_handler(self, event, _):
        try:
            # return self.__response(200, event)
            func = self.__parse(event)
            return self.__response(200, func())
        except HTTPError as e:
            return self.__response(e.status, e.body)
        except:
            print(format_exc())
            return self.__response(500, {"status": "ng", "detail": format_exc()})
            return self.__response(
                500, {"status": "ng", "detail": "internal server error"}
            )

    def __parse(self, event: dict):
        self.event = event
        if "queryStringParameters" in event:
            self.query_params = event["queryStringParameters"]

        if "http" in event["requestContext"]:
            method = event["requestContext"]["http"]["method"]
            path = event["requestContext"]["http"]["path"]
        else:
            method = event["httpMethod"]
            path = event["path"]

        if "cookies" in event:
            self.cookies = event["cookies"]
        elif "Cookie" in event["headers"]:
            self.cookies = event["headers"]["Cookie"].split(";")

        try:
            if event["isBase64Encoded"]:
                body_str = b64decode(event["body"].encode()).decode()
                self.body = loads(body_str)
            else:
                self.body = loads(event["body"])
        except:
            self.body = {}
        # print(path, method)
        d = {"REQUEST_METHOD": method, "PATH_INFO": path}
        func, path_params = self.__router.match(d)
        self.path_params = path_params
        return func

    def set_cookie(self, cookie: str):
        self.__set_cookie = cookie

    def __response(self, status_code: int, body={"status": "ok"}):
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        }
        if len(self.__set_cookie):
            headers["Set-Cookie"] = self.__set_cookie
            headers["Access-Control-Allow-Credentials"] = True
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": dumps(body, ensure_ascii=False, separators=(",", ":")),
            "isBase64Encoded": False,
        }
