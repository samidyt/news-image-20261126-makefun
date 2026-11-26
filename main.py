"""news-image-20261126: one image summing up 26 November 2026 world news.

Copies the bundled entry.png (a 1024x1024 front-page illustration of the
day's six biggest stories) to $MAKEFUN_OUTPUT_DIR/entry.png (default
/output). Standard library only, no network, no randomness, no clock:
every run writes the same bytes.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_png_gate(path):
    """Reject anything over the bounty gate: 1 MiB and 1024x1024 px."""
    if os.path.getsize(path) > 1024 * 1024:
        return "entry.png is over 1 MiB"
    with open(path, "rb") as handle:
        header = handle.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return "entry.png is not a PNG"
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width > 1024 or height > 1024:
        return "entry.png is over 1024x1024"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isfile(SOURCE):
        print("entry.png missing beside main.py", file=sys.stderr)
        return 1
    problem = check_png_gate(SOURCE)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_of(dest) != sha256_of(SOURCE):
        print("copy verification failed", file=sys.stderr)
        return 1
    print(
        "wrote %s (%d bytes, sha256 %s)"
        % (dest, os.path.getsize(dest), sha256_of(dest))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
