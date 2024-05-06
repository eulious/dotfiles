#!/usr/bin/env python3

from json import dumps, loads
from boto3 import client
from typing import Any
from json.decoder import JSONDecodeError


class KVS:
    def __init__(self, bucket: str, key: str):
        self.bucket = bucket
        self.key = key

    def put(self, value: Any):
        return client("s3").put_object(
            Bucket=self.bucket, Key=self.key, Body=dumps(value, ensure_ascii=False)
        )

    def get(self) -> Any:
        obj = client("s3").get_object(Bucket=self.bucket, Key=self.key)
        return self.__parse(obj["Body"].read().decode())

    def __parse(self, value):
        try:
            return loads(value)
        except JSONDecodeError:
            return value
