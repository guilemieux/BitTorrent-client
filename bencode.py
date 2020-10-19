from typing import Tuple

def encode(data: object) -> bytes:
    if isinstance(data, bytes):
        return _encode_bytes(data)
    elif isinstance(data, str):
        return _encode_string(data)
    elif isinstance(data, int):
        return _encode_int(data)
    elif isinstance(data, list):
        return _encode_list(data)
    elif isinstance(data, dict):
        return _encode_dict(data)
    else:
        raise Exception("Type " + str(type(data)) + " can't be bencoded")
    

def _encode_bytes(b: bytes) -> bytes:
    return str(len(b)).encode('ascii') + b':' + b


def _encode_string(s: str) -> bytes:
    return _encode_bytes(s.encode('utf-8'))


def _encode_int(n: int) -> bytes:
    tmp = 'i' + str(n) + 'e'
    return tmp.encode('ascii')


def _encode_list(l: list) -> bytes:
    result = b'l'
    for element in l:
        result += encode(element)
    return result + b'e'


def _encode_dict(d: dict) -> bytes:
    result = b'd'
    for key in d:
        result += encode(key) + encode(d[key])
    return result + b'e'


def decode(bencoding: bytes) -> object:
    result, pos = _decode(bencoding, 0)
    if pos != len(bencoding):
        raise Exception('invalid bencoding (data after valid prefix)')
    return result


def _decode(bencoding: bytes, pos: int) -> Tuple[object, int]:
    if chr(bencoding[pos]).isdigit():
        return _decode_bytes(bencoding, pos)
    elif bencoding[pos] == ord('i'):
        return _decode_int(bencoding, pos)
    elif bencoding[pos] == ord('l'):
        return _decode_list(bencoding, pos)
    elif bencoding[pos] == ord('d'):
        return _decode_dict(bencoding, pos)
    else:
        raise Exception('Invalid bencoding')

def _decode_bytes(bencoding: bytes, pos: int) -> Tuple[bytes, int]:
    colon_pos = pos + bencoding[pos:].index(b':')
    n  = int(bencoding[pos:colon_pos])
    start_pos = colon_pos + 1
    end_pos = start_pos + n
    return bencoding[start_pos:end_pos], end_pos


def _decode_int(bencoding: bytes, pos: int) -> Tuple[int, int]:
    e_pos = pos + bencoding[pos:].index(b'e')
    return int(bencoding[pos + 1:e_pos]), e_pos + 1


def _decode_list(bencoding: bytes, pos: int) -> Tuple[list, int]:
    l = []
    pos += 1
    while bencoding[pos] != ord('e'):
        element, pos = _decode(bencoding, pos)
        l.append(element)
    return l, pos + 1


def _decode_dict(bencoding: bytes, pos: int) -> Tuple[dict, int]:
    d = {}
    pos += 1
    while bencoding[pos] != ord('e'):
        key, pos = _decode(bencoding, pos)
        d[key], pos = _decode(bencoding, pos)
    return d, pos + 1