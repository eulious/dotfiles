#!/usr/bin/env python3

"""
UNIXドメインのソケットで通信

class Command(IntEnum):
    USERS = auto()

@receive(Command.USERS)
def sample_function(data):
    print(data)
    return {"hoge": "aaaa"}

if __name__ == "__main__":
    if argv[1] == "server":
        serve()
    elif argv[1] == "client":
        print(sock(Command.MONDAY, {"hoge": "fuga"}))
"""

from os import remove
from glob import glob
from time import time
from enum import IntEnum
from typing import Any
from struct import pack, unpack
from socket import socket, AF_UNIX, SOCK_STREAM
from pickle import loads, dumps, HIGHEST_PROTOCOL
from asyncio import AbstractEventLoop, create_task, get_event_loop, run, sleep
from os.path import exists

SOCKET_DIR = "/tmp"
SOCKET_NAME = "mysocket"

_method: dict[int, Any] = {}


def sock(command: IntEnum, data=None):
    sock_pattern = f"{SOCKET_DIR}/{SOCKET_NAME}-*.sock"
    sockets = sorted(glob(sock_pattern))
    if not len(sockets):
        raise FileNotFoundError(f"No such file: {sock_pattern}")
    with socket(AF_UNIX, SOCK_STREAM) as sock:
        sock.connect(sockets.pop())
        serialized = dumps(data, protocol=HIGHEST_PROTOCOL)
        sock.sendall(pack(">bbq", 3, command.value, len(serialized)))
        sock.sendall(serialized)
        mode, size = unpack(">bq", sock.recv(9))
        received_data = bytes()
        while (rest := size - len(received_data)) > 0:
            received_data += sock.recv(min(rest, 4096))
        return loads(received_data)


def unixsock(command: IntEnum):
    def decorator(func):
        _method[command.value] = func
        return lambda *args, **kwargs: func(*args, **kwargs)

    return decorator


async def _handle_client(client: socket, loop: AbstractEventLoop):
    with client:
        mode, command, size = unpack(">bbq", await loop.sock_recv(client, 10))
        received_data = bytes()
        while (rest := size - len(received_data)) > 0:
            received_data += await loop.sock_recv(client, min(rest, 4096))
        if data := loads(received_data):
            res = _method[command](data)
        else:
            res = _method[command]()
        serialized = dumps(res, protocol=HIGHEST_PROTOCOL)
        await loop.sock_sendall(client, pack(">bq", 3, len(serialized)))
        await loop.sock_sendall(client, serialized)


async def _run_serve(sock_path: str):
    with socket(AF_UNIX, SOCK_STREAM) as sock:
        sock.setblocking(False)
        sock.bind(sock_path)
        sock.listen()
        loop = get_event_loop()
        print("Server listening...")
        while True:
            client, _ = await loop.sock_accept(sock)
            client.setblocking(False)
            create_task(_handle_client(client, loop))


async def async_serve():
    for fn in glob(f"{SOCKET_DIR}/{SOCKET_NAME}-*.sock"):
        remove(fn)
    sock_path = f"{SOCKET_DIR}/{SOCKET_NAME}-{hex(int(time()*1000))[2:]}.sock"
    create_task(_run_serve(sock_path))
    while True:
        if exists(sock_path):
            break
        await sleep(0.5)
    while True:
        if not exists(sock_path):
            print("Cannot find sock file. terminating...")
            break
        await sleep(1)


def serve():
    run(async_serve())
