from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "__pycache__", "submission_attempts"}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
]


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*"):
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(PROJECT_ROOT).parts):
            continue
        if path.name == ".env":
            files.append(path)
            continue
        files.append(path)
    return files


def main() -> int:
    findings: list[str] = []
    for path in iter_files():
        rel = path.relative_to(PROJECT_ROOT)
        if path.name == ".env":
            findings.append(f"{rel}: .env must not be present for publication")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"{rel}: matched {pattern.pattern}")
    if findings:
        print("Secret scan failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS secret scan found no committed secrets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
