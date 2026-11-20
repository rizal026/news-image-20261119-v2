#!/usr/bin/env python3
"""news-image-20261119 v2 entrypoint.

Ships the pre-rendered front page for Thursday 19 November 2026
(entry.png, 1024x1024) to /output/entry.png, byte for byte.
Both grading runs write identical output: the file is copied in
chunks and the copy is verified by size and SHA-256 before exit.
"""

import hashlib
from pathlib import Path

IMAGE = Path(__file__).resolve().parent / "entry.png"
TARGET = Path("/output/entry.png")
BLOCK = 1 << 16


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(BLOCK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def main():
    expected = sha256_of(IMAGE)
    if IMAGE.stat().st_size > 1048576:
        print("source image over the 1 MiB gate")
        return 1
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with IMAGE.open("rb") as src, TARGET.open("wb") as dst:
        while True:
            block = src.read(BLOCK)
            if not block:
                break
            dst.write(block)
            total += len(block)
    if TARGET.stat().st_size != IMAGE.stat().st_size:
        print("output size mismatch")
        return 1
    if sha256_of(TARGET) != expected:
        print("output hash mismatch")
        return 1
    print(f"wrote {total} bytes to {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
