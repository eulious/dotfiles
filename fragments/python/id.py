#!/usr/bin/env python3

from time import time
from uuid import UUID, SafeUUID
from hashlib import blake2b
from secrets import token_bytes, randbits


# ========= 文字列からIDを作成 ==========
def id62(num):
    uid = ""
    A = [chr(i) for i in [*range(48, 58), *range(65, 91), *range(97, 123)]]
    while num:
        num, m = divmod(num, 62)
        uid = A[m] + uid
    return uid


def id7(num):
    return id62(int(blake2b(str(num).encode(), digest_size=5).hexdigest(), 16))


def blake(text):
    return id62(int(blake2b(text.encode(), digest_size=9).hexdigest(), 16))


# ========= ソート可能なIDの簡単な実装 ==========
def create_id(utime: float = time()):
    return (hex(int(utime * 1000))[2:] + token_bytes(5).hex()).upper()


def id2time(id: str):
    return int(id[:11].lower(), 16) / 1000


# =============== ULID ================
# fmt: off
e = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
d = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 255, 255, 255, 255, 255, 255, 255, 10, 11, 12, 13, 14, 15, 16, 17, 255, 18, 19, 255, 20, 21, 255, 22, 23, 24, 25, 26, 255, 27, 28, 29, 30, 31, 255, 255, 255, 255, 255, 255, 10, 11, 12, 13, 14, 15, 16, 17, 255, 18, 19, 255, 20, 21, 255, 22, 23, 24, 25, 26, 255, 27, 28, 29, 30, 31, 255, 255, 255, 255, 255, 255, 255]

def ulid(utime: float = time()) -> str:
    t, r = int.to_bytes(int(utime * 1000), 6, "big"), token_bytes(10)
    return "".join([e[(t[0] & 224) >> 5], e[(t[0] & 31)], e[(t[1] & 248) >> 3], e[((t[1] & 7) << 2) | ((t[2] & 192) >> 6)], e[((t[2] & 62) >> 1)], e[((t[2] & 1) << 4) | ((t[3] & 240) >> 4)], e[((t[3] & 15) << 1) | ((t[4] & 128) >> 7)], e[(t[4] & 124) >> 2], e[((t[4] & 3) << 3) | ((t[5] & 224) >> 5)], e[(t[5] & 31)], e[(r[0] & 248) >> 3], e[((r[0] & 7) << 2) | ((r[1] & 192) >> 6)], e[(r[1] & 62) >> 1], e[((r[1] & 1) << 4) | ((r[2] & 240) >> 4)], e[((r[2] & 15) << 1) | ((r[3] & 128) >> 7)], e[(r[3] & 124) >> 2], e[((r[3] & 3) << 3) | ((r[4] & 224) >> 5)], e[(r[4] & 31)], e[(r[5] & 248) >> 3], e[((r[5] & 7) << 2) | ((r[6] & 192) >> 6)], e[(r[6] & 62) >> 1], e[((r[6] & 1) << 4) | ((r[7] & 240) >> 4)], e[((r[7] & 15) << 1) | ((r[8] & 128) >> 7)], e[(r[8] & 124) >> 2], e[((r[8] & 3) << 3) | ((r[9] & 224) >> 5)], e[(r[9] & 31)]])


def ulidtime(encoded: str) -> float:
    b = bytes(encoded[:10], "ascii")
    bs = [((d[b[0]] << 5) | d[b[1]]) & 0xFF, ((d[b[2]] << 3) | (d[b[3]] >> 2)) & 0xFF, ((d[b[3]] << 6) | (d[b[4]] << 1) | (d[b[5]] >> 4)) & 0xFF, ((d[b[5]] << 4) | (d[b[6]] >> 1)) & 0xFF, ((d[b[6]] << 7) | (d[b[7]] << 2) | (d[b[8]] >> 3)) & 0xFF, ((d[b[8]] << 5) | (d[b[9]])) & 0xFF]
    return int.from_bytes(bytes(bs), "big") / 1000
# fmt: on

# =============== UUID ver. 7 ================


def uuid7(utime: float = time()) -> UUID:
    uuid_int = (
        (int(utime * 1000) & 0xFFFFFFFFFFFF) << 80
        | randbits(76) & ~(0xC000 << 48)
        | 0x8000 << 48 & ~(0xF000 << 64)
        | 7 << 76
    )
    return UUID(int=uuid_int, is_safe=SafeUUID.unknown)


def uuid7time(uuid_str: str) -> float:
    return int(uuid_str.replace("-", "")[:12], 16) / 1000
