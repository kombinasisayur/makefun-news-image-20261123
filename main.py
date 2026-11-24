#!/usr/bin/env python3
"""Runner for THE HARBOUR POST — news-image-20261123, akun16.

THE HARBOUR POST is a harbour-toned front page for Monday
23 November 2026: white paper, sea-blue ink, coral accents, twelve
numbered cards (the FBI justice-database probe leads), a numbers
box, a dotted map and 27 briefs. This runner's only job is to place
the bundled entry.png into the output folder unchanged.

It is deliberately strict. Before copying, the artwork must match
the recorded byte count and SHA-256 digest, carry the PNG signature
and stay under the competition's 1 MiB ceiling. Anything else is a
hard failure, never a silent copy. Standard library only.
"""

import hashlib
import os
import sys

ART_BYTES = 112727
ART_SHA256 = "5644e8a5788363fc26187b9218062e0a868168b379ae8a084545df73c06b08ed"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SIZE_CAP = 1048576


def load_artwork():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as stream:
        return stream.read()


def verify(data):
    # Collect every problem before failing, so one bad run reports
    # the full picture instead of only the first mismatch.
    problems = []
    if len(data) == 0:
        problems.append("entry.png is empty")
    if data[:8] != PNG_SIGNATURE:
        problems.append("entry.png lacks the PNG signature")
    if len(data) > SIZE_CAP:
        problems.append("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    if len(data) != ART_BYTES:
        problems.append(
            "entry.png has %d bytes, expected %d" % (len(data), ART_BYTES)
        )
    if hashlib.sha256(data).hexdigest() != ART_SHA256:
        problems.append("entry.png sha256 does not match the recorded digest")
    if problems:
        raise SystemExit("; ".join(problems))


def main():
    data = load_artwork()
    verify(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    with open(destination, "wb") as stream:
        stream.write(data)

    sys.stderr.write(
        "harbour-post entry.png -> %s (%d bytes, sha256 %s)\n"
        % (destination, len(data), ART_SHA256)
    )


if __name__ == "__main__":
    main()
