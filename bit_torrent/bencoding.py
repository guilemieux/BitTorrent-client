"""
Encoding and decoding
"""

def bencode(data:object):
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
    

def bdecode(data):
    # TODO
    pass

def bencode_string(s:str):
    return str(len(s)) + ':' + s

def bencode_int(n:int):
    return 'i' + str(n) + 'e'

def bencode_list(l:list):
    bencoding = 'l'
    for element in l:
        bencoding += bencode(element)
    return bencoding + 'e'

def bencode_dict(d:dict):
    bencoding = 'd'
    for key in d:
        bencoding += bencode(key) + bencode(d[key])
    return bencoding + 'e'

print(bencode(lambda x: x**2))