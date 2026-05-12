#!/usr/bin/env python3
"""Search a local godot-docs checkout and print compact snippets."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


DEFAULT_DOCS_DIR = Path.home() / "godot-docs"
GODOT_DOCS_REPO = "https://github.com/godotengine/godot-docs.git"


def resolve_docs_dir(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    env_value = os.environ.get("GODOT_DOCS_DIR")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return DEFAULT_DOCS_DIR


def ensure_docs_dir(path: Path, branch: str | None = None) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "git",
        "clone",
        "--depth",
        "1",
        "--filter=blob:none",
        "--single-branch",
    ]
    if branch:
        command.extend(["--branch", branch])
    command.extend([GODOT_DOCS_REPO, str(path)])
    subprocess.run(command, check=True)


def class_file_name(class_name: str) -> str:
    return f"class_{class_name.lower()}.rst"


def iter_docs(root: Path, glob_pattern: str) -> list[Path]:
    ignored_parts = {".git", "_build", "img", "_static", "_templates"}
    files: list[Path] = []
    for path in root.rglob(glob_pattern):
        if any(part in ignored_parts for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in {".rst", ".md"}:
            files.append(path)
    return files


def heading_for(lines: list[str]) -> str:
    for line in lines[:60]:
        stripped = line.strip()
        if stripped and not stripped.startswith(("..", ":", "|")):
            return stripped
    return "(no heading)"


def score_text(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    score = 0
    for term in terms:
        if term in lowered:
            score += 5
        for token in term.split():
            if token and token in lowered:
                score += 1
    return score


def snippet(lines: list[str], line_index: int, context: int) -> str:
    start = max(0, line_index - context)
    end = min(len(lines), line_index + context + 1)
    selected = []
    for number in range(start, end):
        text = lines[number].rstrip()
        if text:
            selected.append(f"{number + 1}: {text}")
    return "\n".join(selected)


def search_file(path: Path, root: Path, terms: list[str], context: int) -> tuple[int, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0, ""
    lines = text.splitlines()
    best_score = score_text(str(path.relative_to(root)).replace("\\", "/"), terms)
    best_index = 0
    for index, line in enumerate(lines):
        current = score_text(line, terms)
        if current > best_score:
            best_score = current
            best_index = index
    if best_score <= 0:
        return 0, ""
    title = heading_for(lines)
    return best_score, f"{path.relative_to(root)} | {title}\n{snippet(lines, best_index, context)}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--docs-dir", help="Path to godot-docs checkout")
    parser.add_argument("--ensure", action="store_true", help="Clone godot-docs into the resolved docs directory if missing")
    parser.add_argument("--branch", help="Branch/tag to use with --ensure, e.g. stable or master")
    parser.add_argument("--glob", default="*.rst", help="File glob, default: *.rst")
    parser.add_argument("--class", dest="class_name", help="Open a class reference first")
    parser.add_argument("--max-results", type=int, default=8)
    parser.add_argument("--context", type=int, default=2)
    args = parser.parse_args()

    docs_dir = resolve_docs_dir(args.docs_dir)
    if args.ensure:
        ensure_docs_dir(docs_dir, args.branch)
    if not docs_dir.exists():
        raise SystemExit(
            f"godot-docs directory not found: {docs_dir}\n"
            "Clone it with:\n"
            f"  git clone --depth 1 --filter=blob:none {GODOT_DOCS_REPO} {docs_dir}\n"
            "or set GODOT_DOCS_DIR to an existing checkout."
        )

    terms = [term.lower() for term in args.query if term.strip()]
    results: list[tuple[int, str]] = []

    if args.class_name:
        class_path = docs_dir / "classes" / class_file_name(args.class_name)
        if class_path.exists():
            score, output = search_file(class_path, docs_dir, terms or [args.class_name.lower()], args.context)
            results.append((score + 100, output))
        else:
            print(f"Class file not found: {class_path}")

    if not terms and not args.class_name:
        raise SystemExit("Provide a query or --class ClassName")

    for path in iter_docs(docs_dir, args.glob):
        if args.class_name and path.name == class_file_name(args.class_name):
            continue
        score, output = search_file(path, docs_dir, terms, args.context)
        if score:
            results.append((score, output))

    for index, (_, output) in enumerate(sorted(results, key=lambda item: item[0], reverse=True)[: args.max_results], 1):
        print(f"\n## Result {index}\n{output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
