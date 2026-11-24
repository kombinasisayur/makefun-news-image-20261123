#!/usr/bin/env python3
"""THE HARBOUR POST — entry program for news-image-20261123 (akun16).

The artwork is a single-page newspaper front page for Monday
23 November 2026: twelve story cards led by the FBI justice-database
hack probe, a day-in-numbers box, a dotted world map and 27 briefs.
This program is the deliverable runner: it copies the finished
entry.png next to it into the output directory, byte for byte.

Standard library only. The copy is guarded by the exact byte count
and SHA-256 of the artwork, so a swapped or truncated file fails
loudly instead of submitting the wrong page.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 112811
EXPECTED_SHA256 = "f460cee81271a957dd3ad42f47b45f812aa0375662da295dd1259a71475cc175"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
HARD_LIMIT = 1048576  # the competition caps artwork at 1 MiB


def read_artwork(path):
    # Read in one pass; the artwork is small (about 110 KB) and the
    # guards below need the complete byte string anyway.
    with open(path, "rb") as handle:
        return handle.read()


def check_artwork(data):
    if not data:
        raise SystemExit("entry.png is empty")
    if data[:8] != PNG_HEADER:
        raise SystemExit("entry.png does not start with the PNG magic bytes")
    if len(data) > HARD_LIMIT:
        raise SystemExit("entry.png is over the 1 MiB cap: %d bytes" % len(data))
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(
            "entry.png size drifted: got %d bytes, expected %d"
            % (len(data), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.png sha256 mismatch: %s" % digest)
    return digest


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(target_dir, "entry.png")

    payload = read_artwork(source)
    digest = check_artwork(payload)

    os.makedirs(target_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(payload)

    sys.stderr.write(
        "THE HARBOUR POST entry.png copied: %d bytes sha256=%s\n"
        % (len(payload), digest)
    )


if __name__ == "__main__":
    main()
