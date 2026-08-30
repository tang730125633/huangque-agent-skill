#!/usr/bin/env python3
"""Refresh or verify immutable hashes in manifest.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"


def rendered_manifest() -> str:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for item in data["files"]:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe manifest path: {relative}")
        item["sha256"] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = rendered_manifest()
    if args.check:
        if MANIFEST.read_text(encoding="utf-8") != expected:
            print("manifest.json hashes are stale")
            return 1
        return 0
    # Release manifests are hashed and checked on Linux.  Keep their bytes
    # deterministic when this script is run from a Windows checkout.
    MANIFEST.write_bytes(expected.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
