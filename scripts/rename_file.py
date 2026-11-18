"""
Rename files matching a filename stem and update references in project documents.

Usage: python scripts/rename_file.py <old_stem> <new_stem> [--dry-run]
"""

import argparse
import os
import re
import uuid
from typing import Set

IGNORED_DIRS: Set[str] = {".git", "out", "__pycache__", ".vscode", ".idea", ".venv", "venv", "node_modules"}
REFERENCE_EXTENSIONS = (".tex", ".yaml", ".yml", ".json")


def should_skip_dir(dirname: str) -> bool:
    return dirname in IGNORED_DIRS or dirname.startswith("_minted")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename files by stem and update references in .tex/.yaml/.json files."
    )
    parser.add_argument("old_filename", help="Old filename stem (without extension).")
    parser.add_argument("new_filename", help="New filename stem (without extension).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying or renaming any files.",
    )
    args = parser.parse_args()

    old_stem = args.old_filename
    new_stem = args.new_filename
    for stem in (old_stem, new_stem):
        if not stem or stem in (".", "..") or any(c in stem for c in '/\\:*?"<>|'):
            parser.error("Provide a filename stem, without directories or invalid filename characters.")
    if old_stem == new_stem:
        return
    root_dir = os.getcwd()

    renames = []
    references = []
    destinations = set()
    names = set()
    for directory, subdirs, filenames in os.walk(root_dir):
        subdirs[:] = [d for d in subdirs if not should_skip_dir(d)]
        for filename in sorted(filenames):
            path = os.path.join(directory, filename)
            if filename.lower().endswith(REFERENCE_EXTENSIONS):
                references.append(path)
            stem, extension = os.path.splitext(filename)
            if stem.casefold() != old_stem.casefold():
                continue
            target = os.path.join(directory, new_stem + extension)
            key = os.path.normcase(target)
            if key in destinations:
                parser.error(f"Several files would be renamed to {target}")
            destinations.add(key)
            if os.path.lexists(target) and os.path.normcase(path) != key:
                parser.error(f"Destination already exists: {target}")
            names.add(filename)
            renames.append((path, target))
    if not renames:
        return

    alternatives = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    filename_pattern = re.compile(rf"(?<![\w.-])(?:{alternatives})(?![\w.-])", re.IGNORECASE)
    input_pattern = re.compile(
        rf"(\\(?:input|include)\s*\{{(?:[^{{}}\n]*/)?){re.escape(old_stem)}(?=\s*\}})",
        re.IGNORECASE,
    )
    # Only complete filename/path scalar values are references in structured data.
    # Exclude mapping keys, including quoted JSON keys.
    scalar_pattern = re.compile(
        rf"""(?P<prefix>(?:^|[:\[,\-])\s*["']?(?:[^"'\n{{}}\[\],]*[/\\])?)"""
        rf"""(?P<name>{alternatives})(?=["']?\s*(?:[,}}\]#]|$))""",
        re.IGNORECASE | re.MULTILINE,
    )
    mode_prefix = "[DRY-RUN] " if args.dry_run else ""
    reference_updates = []
    for file_path in references:
        try:
            with open(file_path, encoding="utf-8", newline="") as stream:
                content = stream.read()
        except (OSError, UnicodeDecodeError) as error:
            parser.error(f"Cannot read {file_path} as UTF-8: {error}")
        if file_path.lower().endswith(".tex"):
            updated = filename_pattern.sub(lambda m: new_stem + os.path.splitext(m[0])[1], content)
            updated = input_pattern.sub(lambda m: m[1] + new_stem, updated)
        else:
            updated = scalar_pattern.sub(
                lambda m: m["prefix"] + new_stem + os.path.splitext(m["name"])[1], content
            )
        if updated != content:
            reference_updates.append((file_path, updated))

    for file_path, new_content in reference_updates:
        rel_path = os.path.relpath(file_path, root_dir)
        if not args.dry_run:
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                f.write(new_content)
        print(f"{mode_prefix}[Content Updated] inside: {rel_path}")

    for file_path, new_file_path in renames:
        rel_path = os.path.relpath(file_path, root_dir)
        if not args.dry_run:
            if os.path.basename(file_path).casefold() == os.path.basename(new_file_path).casefold():
                temp_path = os.path.join(
                    os.path.dirname(file_path),
                    f".rename-{uuid.uuid4().hex}{os.path.splitext(file_path)[1]}",
                )
                os.rename(file_path, temp_path)
                try:
                    os.rename(temp_path, new_file_path)
                except OSError:
                    os.rename(temp_path, file_path)
                    raise
            else:
                os.rename(file_path, new_file_path)
        print(f"{mode_prefix}[File Renamed] {rel_path} -> {os.path.basename(new_file_path)}")


if __name__ == "__main__":
    main()
