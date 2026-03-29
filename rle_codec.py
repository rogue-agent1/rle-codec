#!/usr/bin/env python3
"""rle_codec: Run-length encoding/decoding."""
import sys

def encode(data):
    if not data: return []
    result = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1]:
            count += 1
        else:
            result.append((data[i-1], count))
            count = 1
    result.append((data[-1], count))
    return result

def decode(runs):
    return "".join(c * n for c, n in runs)

def encode_bytes(data: bytes) -> bytes:
    if not data: return b""
    result = bytearray()
    i = 0
    while i < len(data):
        val = data[i]
        count = 1
        while i + count < len(data) and data[i+count] == val and count < 255:
            count += 1
        result.append(count)
        result.append(val)
        i += count
    return bytes(result)

def decode_bytes(data: bytes) -> bytes:
    result = bytearray()
    for i in range(0, len(data), 2):
        count = data[i]
        val = data[i+1]
        result.extend([val] * count)
    return bytes(result)

def test():
    assert encode("aaabbbcc") == [("a",3),("b",3),("c",2)]
    assert decode([("a",3),("b",3),("c",2)]) == "aaabbbcc"
    assert encode("abc") == [("a",1),("b",1),("c",1)]
    assert encode("") == []
    assert decode([]) == ""
    # Bytes
    data = b"\x00\x00\x00\xff\xff\x42"
    assert decode_bytes(encode_bytes(data)) == data
    assert decode_bytes(encode_bytes(b"")) == b""
    # Long run
    long_data = "a" * 300
    runs = encode(long_data)
    assert runs == [("a", 300)]
    assert decode(runs) == long_data
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: rle_codec.py test")
