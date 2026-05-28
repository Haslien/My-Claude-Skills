#!/usr/bin/env python3
"""
index_md.py — scan a directory tree for .md files and generate a skeleton index.

For each .md file, records:
- relative path
- created date (first git commit that added the file; falls back to filesystem birth time)
- last modified date (most recent git commit that touched the file; falls back to mtime)

Writes a single flat table sorted by modified date (newest first), with "TBD" in
the description column. Claude is expected to then walk the table and fill each
description in one at a time (read file -> update row -> save -> next), so the
context stays focused on one document at a time.

If the output file already exists, descriptions for rows whose "modified" date
has not changed are preserved on re-run.

Usage:
    python index_md.py [TARGET_DIR] [--output PATH] [--name FILENAME]

Defaults:
    TARGET_DIR     current working directory
    --name         MD_INDEX.md (written at the root of TARGET_DIR)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Directories never worth scanning for documentation .md files.
# Dotfolders not in this set (e.g. .github, .claude) are kept — they often
# contain real docs.
DEFAULT_EXCLUDES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "out",
    "coverage",
    ".turbo",
    ".cache",
    "target",
    "vendor",
    ".idea",
    ".gradle",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*\[(?P<path>[^\]]+)\]\([^)]+\)\s*\|"
    r"\s*(?P<created>[^|]*?)\s*\|\s*(?P<modified>[^|]*?)\s*\|"
    r"\s*(?P<desc>.*?)\s*\|\s*$"
)


def find_git_root(start: Path) -> Path | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def git_dates(path: Path, repo_root: Path) -> tuple[str | None, str | None]:
    """Return (created, modified) as YYYY-MM-DD from git history, or (None, None)
    if the file is untracked."""
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return None, None

    try:
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%aI", "--", str(rel)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

    lines = [l for l in result.stdout.strip().splitlines() if l]
    if not lines:
        return None, None

    # git log lists newest first; oldest is the last line.
    modified = lines[0][:10]
    created = lines[-1][:10]
    return created, modified


def fs_dates(path: Path) -> tuple[str, str]:
    stat = path.stat()
    birth = getattr(stat, "st_birthtime", stat.st_ctime)
    created = datetime.fromtimestamp(birth).strftime("%Y-%m-%d")
    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
    return created, modified


def get_dates(path: Path, repo_root: Path | None) -> tuple[str, str]:
    if repo_root is not None:
        c, m = git_dates(path, repo_root)
        if c and m:
            return c, m
    return fs_dates(path)


def find_md_files(root: Path, output_path: Path) -> list[Path]:
    found: list[Path] = []
    output_resolved = output_path.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDES]
        for name in filenames:
            if not name.lower().endswith(".md"):
                continue
            if name.startswith("."):
                continue
            path = Path(dirpath) / name
            if path.resolve() == output_resolved:
                continue
            found.append(path)
    return found


def parse_existing(output_path: Path) -> dict[str, tuple[str, str]]:
    """Return {relative_path: (modified_date, description)} from an existing index."""
    if not output_path.exists():
        return {}
    previous: dict[str, tuple[str, str]] = {}
    for line in output_path.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        previous[match.group("path")] = (
            match.group("modified"),
            match.group("desc"),
        )
    return previous


def render(target: Path, entries: list[dict], git_root: Path | None) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    source = "git history" if git_root else "filesystem timestamps"
    lines = [
        f"# Markdown Index: {target.name}",
        "",
        f"> Auto-generated index of every `.md` file under `{target}`.",
        f"> Last scanned: {today} · Source: {source} · Total: {len(entries)} files",
        "",
        "> **How descriptions get filled:** rows start with `TBD`. Claude walks the table",
        "> top-down, reads one file at a time, replaces that row's `TBD` with a one-line",
        "> description, saves, and moves on. This avoids losing context on large repos.",
        "",
        "| # | File | Created | Modified | Description |",
        "|---|------|---------|----------|-------------|",
    ]
    for i, e in enumerate(entries, 1):
        desc = e["desc"].replace("|", "\\|")
        rel = e["rel"]
        lines.append(
            f"| {i} | [{rel}]({rel}) | {e['created']} | {e['modified']} | {desc} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a skeleton index of all .md files in a directory tree."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Directory to scan (default: current working directory).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Absolute or relative path for the output index file.",
    )
    parser.add_argument(
        "--name",
        default="MD_INDEX.md",
        help="Output filename when --output is not given (default: MD_INDEX.md).",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"Not a directory: {target}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = (target / args.name).resolve()

    git_root = find_git_root(target)
    previous = parse_existing(output_path)

    md_files = find_md_files(target, output_path)

    entries = []
    for path in md_files:
        rel = path.resolve().relative_to(target).as_posix()
        created, modified = get_dates(path, git_root)
        prev = previous.get(rel)
        if prev and prev[0] == modified and prev[1].strip() and prev[1].strip() != "TBD":
            desc = prev[1]
        else:
            desc = "TBD"
        entries.append(
            {
                "path": path,
                "rel": rel,
                "created": created,
                "modified": modified,
                "desc": desc,
            }
        )

    entries.sort(key=lambda e: (e["modified"], e["rel"]), reverse=True)

    output_path.write_text(render(target, entries, git_root), encoding="utf-8")

    tbd_count = sum(1 for e in entries if e["desc"] == "TBD")
    reused = len(entries) - tbd_count
    print(f"Wrote {output_path}")
    print(f"Indexed {len(entries)} .md files ({tbd_count} TBD, {reused} preserved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
