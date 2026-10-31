#!/usr/bin/env python3
"""Validate synthetic replay data without network or cloud access."""
import json
import sys
from pathlib import Path


def validate(data):
    if data.get("kind") != "Synthetic example":
        raise ValueError("fixture must be explicitly synthetic")
    groups = data["groups"]
    if len(groups) != 2 or {g["key"] for g in groups} != {"A", "B"}:
        raise ValueError("exactly groups A and B are required")
    seen, messages = set(), []
    for group in groups:
        expected, actual = group["expected"], group["actual"]
        count = group["resource_count"]
        if len(expected) != len(set(expected)) or len(actual) != len(set(actual)):
            raise ValueError(f'{group["key"]}: duplicate ResourceId')
        if len(actual) != count or len(expected) != count:
            raise ValueError(f'{group["key"]}: ResourceCount mismatch')
        if set(expected) != set(actual):
            raise ValueError(f'{group["key"]}: set mismatch despite equal count')
        if seen.intersection(actual):
            raise ValueError("groups overlap")
        seen.update(actual)
        messages.append(f'{group["key"]}: {count} resources, exact set match')
    return messages + ["PASS: groups are disjoint; synthetic fixture only"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 examples/verify_replay.py examples/replay-fixture.json", file=sys.stderr)
        sys.exit(2)
    try:
        for line in validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))):
            print(line)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
