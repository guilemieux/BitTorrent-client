"""
Encoding and decoding
"""
from typing import Tuple

def bencode(data: object) -> str:
    if isinstance(data, str):
        return bencode_string(data)
    elif isinstance(data, int):
        return bencode_int(data)
    elif isinstance(data, list):
        return bencode_list(data)
    elif isinstance(data, dict):
        return bencode_dict(data)
    else:
        raise Exception("Type " + str(type(data)) + " can't be bencoded")
    

def bdecode(encoding: str):
    result, pos = bdecode_be(encoding, 0)
    if pos != len(encoding):
        raise Exception('invalid bencoding (data after valid prefix)')
    return result

def read(filename: str):
    with open(filename, 'rb') as file:
        return bdecode(file.read())

def bencode_string(s:str) -> str:
    return str(len(s)) + ':' + s

def bencode_int(n:int) -> str:
    return 'i' + str(n) + 'e'

def bencode_list(l:list) -> str:
    bencoding = 'l'
    for element in l:
        bencoding += bencode(element)
    return bencoding + 'e'

def bencode_dict(d:dict) -> str:
    bencoding = 'd'
    for key in d:
        bencoding += bencode(key) + bencode(d[key])
    return bencoding + 'e'

def bdecode_be(s:str, pos:int) -> Tuple[str, int]:
    if chr(s[pos]).isdigit(): return bdecode_string(s, pos)
    elif s[pos] == ord('i'): return bdecode_int(s, pos)
    elif s[pos] == ord('l'): return bdecode_list(s, pos)
    elif s[pos] == ord('d'): return bdecode_dict(s, pos)
    else: raise Exception('Invalid bencoding')

def bdecode_string(s:str, pos:int) -> Tuple[str, int]:
    colon_pos = pos + s[pos:].index(b':')
    n = int(s[pos:colon_pos])
    start_pos = colon_pos + 1
    end_pos = start_pos + n
    return s[start_pos:end_pos], end_pos

def bdecode_int(s:str, pos:int) -> Tuple[int, int]:
    e_pos = pos + s[pos:].index(b'e')
    return int(s[pos + 1:e_pos]), e_pos + 1

def bdecode_list(s:str, pos:int) -> Tuple[list, int]:
    l = []
    pos += 1
    while s[pos] != ord('e'):
        element, pos = bdecode_be(s, pos)
        l.append(element)
    return l, pos + 1

def bdecode_dict(s:str, pos:int) -> Tuple[dict, int]:
    d = {}
    pos += 1
    while s[pos] != ord('e'):
        key, pos = bdecode_be(s, pos)
        d[key], pos = bdecode_be(s, pos)
    return d, pos + 1
