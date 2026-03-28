#!/usr/bin/env python3
"""rle_codec - Run-length encoding/decoding."""
import sys

def encode(data):
    if not data: return ""
    result = []; count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1]: count += 1
        else: result.append((data[i-1], count)); count = 1
    result.append((data[-1], count))
    return "".join(f"{c}{n}" if n > 1 else c for c, n in result)

def decode(data):
    import re
    result = []
    for m in re.finditer(r"([^0-9])(\d*)", data):
        c, n = m.group(1), m.group(2)
        result.append(c * (int(n) if n else 1))
    return "".join(result)

def encode_bytes(data):
    if not data: return b""
    result = bytearray(); i = 0
    while i < len(data):
        byte = data[i]; count = 1
        while i + count < len(data) and data[i+count] == byte and count < 255: count += 1
        result.extend([count, byte]); i += count
    return bytes(result)

def decode_bytes(data):
    result = bytearray()
    for i in range(0, len(data), 2):
        result.extend([data[i+1]] * data[i])
    return bytes(result)

if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: rle_codec.py <encode|decode> <text|file>"); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "encode": print(encode(sys.argv[2]))
    elif cmd == "decode": print(decode(sys.argv[2]))
    elif cmd == "encode-file":
        data = open(sys.argv[2], "rb").read(); enc = encode_bytes(data)
        out = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2] + ".rle"
        open(out, "wb").write(enc); print(f"{len(data)} → {len(enc)} ({len(enc)/len(data)*100:.1f}%)")
