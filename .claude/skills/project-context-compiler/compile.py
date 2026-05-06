"""
Project Context Compiler.

Reads a JSON config from ./projects/<name>.json and writes a single combined
text file to ./output/<name>.txt containing every selected file's contents,
wrapped with optional headers/footers. Designed for pasting an entire project
into an LLM in one go.

Config schema:
    title           str   - shown as a header in the output
    absolute_path   str   - root directory of the target project
    start_prompt    str   - text written once at the very top
    start_text      str   - per-file header template (use {file})
    stop_text       str   - per-file footer template (use {file})
    files           list  - relative paths or glob patterns (e.g. "src/**")
    use_gitignore   bool  - read the target project's .gitignore (default true)
    ignore          list  - extra .gitignore-style patterns to exclude

Usage:
    python compile.py my-project.json
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import mimetypes
import os
import subprocess
from typing import Callable, Iterable

try:
    import pathspec
except ImportError:
    pathspec = None

try:
    from PIL import Image
except ImportError:
    Image = None


OK = "[ok]"
WARN = "[warn]"
ERR = "[err]"

TEXT_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".txt", ".html",
    ".css", ".scss", ".sass", ".yml", ".yaml", ".toml", ".py",
    ".cjs", ".mjs", ".graphql", ".gql", ".sh", ".bash", ".env",
    ".gitignore", ".gitattributes", ".sql", ".rs", ".go", ".java",
    ".kt", ".rb", ".php", ".c", ".cpp", ".h", ".hpp", ".swift",
}


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def human_duration(seconds: float) -> str:
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {sec}s"
    if m:
        return f"{m}m {sec}s"
    return f"{sec}s"


def ffprobe_duration(path: str) -> float | None:
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            capture_output=True, text=True, check=True,
        )
        out = result.stdout.strip()
        return float(out) if out else None
    except Exception:
        return None


def is_text_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(path)
    if mime and (mime.startswith("text/") or mime in ("application/json", "application/xml")):
        return True
    try:
        with open(path, "rb") as f:
            f.read(4096).decode("utf-8")
        return True
    except Exception:
        return False


def media_info(path: str) -> str | None:
    size_str = human_size(os.path.getsize(path))
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        return None
    if mime.startswith("image/"):
        if Image is not None:
            try:
                with Image.open(path) as im:
                    return f"image {im.width}x{im.height}px, {size_str}"
            except Exception:
                pass
        return f"image, {size_str}"
    if mime.startswith("video/"):
        dur = ffprobe_duration(path)
        if dur is not None:
            return f"video {size_str}, {human_duration(dur)}"
        return f"video, {size_str}"
    return None


def build_ignore_matcher(repo_root: str, use_gitignore: bool, extra: Iterable[str]) -> Callable[[str], bool]:
    patterns: list[str] = []

    if use_gitignore:
        gi = os.path.join(repo_root, ".gitignore")
        if os.path.isfile(gi):
            try:
                with open(gi, "r", encoding="utf-8") as f:
                    patterns.extend(line.rstrip("\n") for line in f)
                print(f"{OK} read .gitignore from {gi}")
            except Exception as e:
                print(f"{WARN} could not read .gitignore: {e}")

    patterns.extend(str(p) for p in (extra or []))

    if pathspec is not None:
        spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        return lambda rel: spec.match_file(rel.replace(os.sep, "/"))

    norm: list[str] = []
    for pat in patterns:
        pat = pat.strip()
        if not pat or pat.startswith("#"):
            continue
        if pat.endswith("/"):
            pat += "**"
        norm.append(pat.replace("\\", "/"))

    def fallback(rel: str) -> bool:
        posix = rel.replace(os.sep, "/")
        return any(fnmatch.fnmatch(posix, p) for p in norm)

    return fallback


def expand_files(root: str, requested: list[str], is_ignored: Callable[[str], bool]) -> tuple[list[str], list[str]]:
    included: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()

    for raw in requested:
        entry = (raw or "").strip()
        if not entry:
            continue

        pattern = entry + "**" if entry.endswith("/") else entry
        has_glob = any(c in pattern for c in ("*", "?", "["))

        if has_glob:
            matches = sorted(
                m for m in glob.glob(os.path.join(root, pattern), recursive=True)
                if os.path.isfile(m)
            )
            if not matches:
                print(f"{WARN} no matches: {entry}")
                missing.append(entry)
                continue
            kept = 0
            for full in matches:
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                if is_ignored(rel):
                    continue
                if rel not in seen:
                    seen.add(rel)
                    included.append(rel)
                    kept += 1
            print(f"{OK} {entry} -> {kept} file(s)")
        else:
            full = os.path.join(root, entry)
            if not os.path.isfile(full):
                print(f"{ERR} not found: {entry}")
                missing.append(entry)
                continue
            rel = entry.replace("\\", "/")
            if is_ignored(rel):
                print(f"{WARN} ignored: {rel}")
                continue
            if rel not in seen:
                seen.add(rel)
                included.append(rel)
                print(f"{OK} {rel}")

    return included, missing


def render_template(tpl: str, rel_path: str) -> str:
    if not tpl:
        return ""
    return tpl.replace("{file}", rel_path) if "{file}" in tpl else f'{tpl} "{rel_path}"'


def compile_project(config_filename: str) -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "projects", config_filename)
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    title = (cfg.get("title") or "").strip()
    abs_path = (cfg.get("absolute_path") or "").strip()
    start_prompt = cfg.get("start_prompt", "")
    start_tpl = cfg.get("start_text", "")
    stop_tpl = cfg.get("stop_text", "")
    files_list = cfg.get("files", [])
    use_gitignore = cfg.get("use_gitignore", True)
    extra_ignore = cfg.get("ignore", []) or []

    if not abs_path:
        raise ValueError("'absolute_path' must not be empty")
    if not os.path.isdir(abs_path):
        raise FileNotFoundError(f"absolute_path does not exist: {abs_path}")
    if not isinstance(files_list, list) or not files_list:
        raise ValueError("'files' must be a non-empty list")

    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(config_filename))[0]
    output_path = os.path.join(output_dir, f"{base_name}.txt")

    is_ignored = build_ignore_matcher(abs_path, use_gitignore, extra_ignore)

    print(f"\nCompiling project root: {abs_path}")
    included, missing = expand_files(abs_path, files_list, is_ignored)
    print(f"\nSelection: {len(included)} file(s), {len(missing)} unmatched entry(s)")

    written = 0
    with open(output_path, "w", encoding="utf-8") as out:
        if start_prompt:
            out.write(start_prompt.rstrip() + "\n\n")
        if title:
            out.write(f"Project: {title}\n\n")

        for rel in included:
            full = os.path.join(abs_path, rel)
            header = render_template(start_tpl, rel)
            footer = render_template(stop_tpl, rel)
            if header:
                out.write(header + "\n")

            try:
                if is_text_file(full):
                    with open(full, "r", encoding="utf-8") as src:
                        out.write(src.read())
                    print(f"{OK} text: {rel}")
                else:
                    info = media_info(full) or f"binary file, {human_size(os.path.getsize(full))}"
                    out.write(f"*** {info} ***\n")
                    print(f"{OK} meta: {rel} -> {info}")
            except Exception as e:
                out.write(f"*** ERROR: could not read {rel}: {e} ***\n")
                print(f"{ERR} read failed: {rel} -> {e}")

            if footer:
                out.write(footer)
            out.write("\n\n")
            written += 1

    print(f"\n{OK} done. Output: {output_path}")
    print(f"{OK} files written: {written}")
    if missing:
        print(f"{WARN} unmatched entries:")
        for m in missing:
            print(f"   - {m}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatenate project files into one .txt for LLM context."
    )
    parser.add_argument("project_json", help="JSON file in projects/ (e.g. my-project.json)")
    args = parser.parse_args()

    try:
        compile_project(args.project_json)
    except Exception as e:
        print(f"{ERR} {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
