#!/usr/bin/env python3
"""
Enforce 100-line limit on all .py and .html files.
Exits with code 1 if any file exceeds the limit.
Usage: python scripts/check_line_count.py [path]
"""
import sys
from pathlib import Path

LIMIT = 100
EXTENSIONS = {".py", ".html"}
IGNORE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "migrations",
    ".aws-sam", "node_modules", ".pytest_cache",
}
# Files allowed to exceed limit (generated or config files)
IGNORE_FILES = {
    "settings.py", "conftest.py",
}

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
violations = []

for path in root.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix not in EXTENSIONS:
        continue
    if any(part in IGNORE_DIRS for part in path.parts):
        continue
    if path.name in IGNORE_FILES:
        continue

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    count = len(lines)
    if count > LIMIT:
        violations.append((path, count))

if violations:
    print(f"\n❌  Files exceeding {LIMIT}-line limit:\n")
    for path, count in sorted(violations):
        print(f"  {path}  →  {count} lines  (over by {count - LIMIT})")
    print(f"\n  Total violations: {len(violations)}")
    print(f"  Split large files into smaller, focused modules.\n")
    sys.exit(1)
else:
    print(f"✅  All files are within the {LIMIT}-line limit.")
    sys.exit(0)
