#!/usr/bin/env python3

"""
スレッドセーフな共有オブジェクト
multiprocessing.Valueのシングルプロセス版
"""

from threading import Lock
from typing import Generic, TypeVar

T = TypeVar("T")


class Shared(Generic[T]):
    def __init__(self, value: T = None):
        self._value = value
        self._lock = Lock()

    @property
    def value(self) -> T:
        with self._lock:
            return self._value

    @value.setter
    def value(self, new_value: T):
        with self._lock:
            self._value = new_value
