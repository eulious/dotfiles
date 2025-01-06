#!/usr/bin/env python3

"""python-dotenvの代わり"""

from re import match
from os import environ

for line in [x.strip() for x in open(".env").readlines()]:
    if line and not line.startswith("#") and "=" in line:
        key, value = [x.strip() for x in line.split("=", 1)]
        environ[key] = value[1:-1] if match(r'["\']', value) else value
