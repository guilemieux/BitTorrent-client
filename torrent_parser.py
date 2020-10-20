import bencode as be

def parse_torrent_file(filename: str):
    with open(filename, 'rb') as f:
        data = f.read()

    d = be.decode(data)

    # Convert all keys to utf-8 strings
    torrent = decode_dict_utf8(d)

    return torrent


def decode_dict_utf8(d: dict) -> dict:
    result = {}
    for key in d:
        decoded_key = key.decode('utf-8')
        value = d[key]
        if decoded_key == 'pieces':
            result[decoded_key] = parse_pieces(value)
        elif isinstance(value, bytes):
            result[decoded_key] = value.decode('utf-8')
        elif isinstance(value, int):
            result[decoded_key] = value
        elif isinstance(d[key], dict):
            result[decoded_key] = decode_dict_utf8(value)
        elif isinstance(value, list):
            result[decoded_key] = decode_list_utf8(value)
    
    return result


def decode_list_utf8(l: list) -> list:
    result = []
    for e in l:
        if isinstance(e, bytes):
            result.append(e.decode('utf-8'))
        elif isinstance(e, int):
            result.append(e)
        elif isinstance(e, list):
            result.append(decode_list_utf8(e))
        elif isinstance(e, dict):
            result.append(decode_dict_utf8(e))
    
    return result
    

def parse_pieces(b: bytes) -> list:
    l = []
    for i in range(0, len(b), 20):
        hash = b[i:i + 20].hex()
        l.append(hash)
    return l


if __name__ == "__main__":
    r = parse_torrent_file('torrent-file-examples/wired-cd.torrent')
    import json
    with open('output.json', 'w') as f:
        f.write(json.dumps(r, indent=4, default=str))
