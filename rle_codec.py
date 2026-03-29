#!/usr/bin/env python3
"""rle_codec - Run-length encoding and decoding."""
import sys, argparse, json

def encode(data):
    if not data: return []
    runs = []
    current, count = data[0], 1
    for ch in data[1:]:
        if ch == current:
            count += 1
        else:
            runs.append((current, count))
            current, count = ch, 1
    runs.append((current, count))
    return runs

def decode(runs):
    return "".join(ch * count for ch, count in runs)

def to_string(runs):
    return "".join(f"{ch}{count}" if count > 1 else ch for ch, count in runs)

def from_string(s):
    runs, i = [], 0
    while i < len(s):
        ch = s[i]; i += 1
        num = ""
        while i < len(s) and s[i].isdigit():
            num += s[i]; i += 1
        runs.append((ch, int(num) if num else 1))
    return runs

def main():
    p = argparse.ArgumentParser(description="RLE codec")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("encode"); e.add_argument("text")
    d = sub.add_parser("decode"); d.add_argument("encoded")
    args = p.parse_args()
    if args.cmd == "encode":
        runs = encode(args.text)
        encoded = to_string(runs)
        ratio = len(encoded) / len(args.text) if args.text else 0
        print(json.dumps({"input": args.text, "encoded": encoded, "runs": len(runs), "ratio": round(ratio, 3)}))
    elif args.cmd == "decode":
        runs = from_string(args.encoded)
        decoded = decode(runs)
        print(json.dumps({"encoded": args.encoded, "decoded": decoded, "length": len(decoded)}))
    else: p.print_help()

if __name__ == "__main__": main()
