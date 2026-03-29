#!/usr/bin/env python3
"""rle_codec - Run-length encoding variants."""
import sys, argparse, json

def rle_encode(data):
    if not data: return []
    runs = []; current = data[0]; count = 1
    for c in data[1:]:
        if c == current and count < 255: count += 1
        else: runs.append((count, current)); current = c; count = 1
    runs.append((count, current))
    return runs

def rle_decode(runs):
    return "".join(c * n for n, c in runs)

def rle_encode_bytes(data):
    encoded = []
    for n, c in rle_encode(data):
        encoded.extend([n, ord(c) if isinstance(c, str) else c])
    return bytes(encoded)

def packbits_encode(data):
    """Apple PackBits-style encoding."""
    result = []; i = 0; n = len(data)
    while i < n:
        # Check for run
        run_len = 1
        while i + run_len < n and run_len < 128 and data[i + run_len] == data[i]:
            run_len += 1
        if run_len >= 3:
            result.append(257 - run_len); result.append(ord(data[i]) if isinstance(data[i], str) else data[i])
            i += run_len
        else:
            # Literal run
            lit_start = i
            while i < n and i - lit_start < 128:
                if i + 2 < n and data[i] == data[i+1] == data[i+2]: break
                i += 1
            lit_len = i - lit_start
            if lit_len > 0:
                result.append(lit_len - 1)
                for j in range(lit_start, i):
                    result.append(ord(data[j]) if isinstance(data[j], str) else data[j])
    return bytes(result)

def packbits_decode(data):
    result = []; i = 0
    while i < len(data):
        n = data[i]; i += 1
        if n < 128:
            count = n + 1
            result.extend(data[i:i+count]); i += count
        elif n > 128:
            count = 257 - n
            result.extend([data[i]] * count); i += 1
    return bytes(result)

def analyze(original, compressed):
    orig_size = len(original)
    comp_size = len(compressed)
    return {"original": orig_size, "compressed": comp_size,
            "ratio": round(comp_size/orig_size, 3) if orig_size else 0,
            "savings": round((1-comp_size/orig_size)*100, 1) if orig_size else 0}

def main():
    p = argparse.ArgumentParser(description="Run-length encoding")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        tests = ["AAABBBCCDDDDDDEEEF", "ABCDEFG", "AAAAAAAAAAAA",
                 "ABABABABABAB", "A"*100 + "B"*50 + "C"*25]
        print("=== Basic RLE ===")
        for text in tests:
            runs = rle_encode(text)
            decoded = rle_decode(runs)
            ok = decoded == text
            ratio = sum(2 for _ in runs) / len(text)
            print(f"[{'OK' if ok else 'FAIL'}] \"{text[:30]}{'...' if len(text)>30 else ''}\" runs={len(runs)} ratio={ratio:.2f}")
        print("\n=== PackBits ===")
        for text in tests:
            packed = packbits_encode(text)
            unpacked = packbits_decode(packed)
            decoded_str = "".join(chr(b) for b in unpacked)
            ok = decoded_str == text
            stats = analyze(text, packed)
            print(f"[{'OK' if ok else 'FAIL'}] savings={stats['savings']}%")
    else: p.print_help()
if __name__ == "__main__": main()
