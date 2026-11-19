#!/usr/bin/env python3
"""Entry program for the v2 front page: copy entry.png to /output/entry.png.

Standard library only, so it runs as-is in the grader's container. The
image itself is built ahead of time by render.py (Pillow, sheet.webp plus
three data-graphics drawn in code) and shipped in this repository. Outside
the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()[:12]
    print("wrote", dst, os.path.getsize(dst), "bytes, sha256", digest)


if __name__ == "__main__":
    main()
