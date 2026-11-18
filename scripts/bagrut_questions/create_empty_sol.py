"""Generate Bagrut solution stubs from question images or PDFs."""

import argparse
from functools import lru_cache
import os
from pathlib import Path
import sys
from typing import List

sys.path.insert(0, os.path.dirname(__file__))
from utils import SUPPORTED_EXTENSIONS, parse_filename


TEMPLATE_PATH = Path(__file__).resolve().with_name("empty_sol_template.tex")

# Default folders processed in batch mode
FOLDERS: List[str] = [
    "bagrut_questions/computational_models",
    "bagrut_questions/basics",
    "bagrut_questions/oop",
]


@lru_cache(maxsize=1)
def load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def select_variant(template: str, extension: str) -> str:
    """Keep the template lines marked for this media kind (%PDF / %IMAGE) and drop the others."""
    keep, drop = ("%PDF ", "%IMAGE ") if extension == "pdf" else ("%IMAGE ", "%PDF ")
    lines = []
    for line in template.splitlines(keepends=True):
        if line.startswith(keep):
            lines.append(line[len(keep):])
        elif not line.startswith(drop):
            lines.append(line)
    return "".join(lines)


def render(template: str, media: Path, folder: str) -> str:
    _, year, model, number, extension = parse_filename(media.name)
    path = f"../../../bagrut_questions/{folder}/{media.name}"
    return (select_variant(template, extension).replace("[[MEDIA_PATH]]", path)
            .replace("[[YEAR]]", year).replace("[[MODEL]]", model).replace("[[NUMBER]]", number))


def media_groups(directory: Path):
    groups = {}
    for path in sorted(directory.iterdir()):
        if path.is_file() and parse_filename(path.name)[0] != "UNKNOWN":
            groups.setdefault(path.stem.casefold(), []).append(path)
    for siblings in groups.values():
        siblings.sort(key=lambda p: SUPPORTED_EXTENSIONS.index(p.suffix[1:].lower()))
    return groups


def process_group(siblings, force: bool) -> None:
    media = siblings[0]
    try:
        folder = media.resolve().parent.relative_to(Path("bagrut_questions").resolve()).as_posix()
    except ValueError:
        print(f"Skipping (not under bagrut_questions/; run from the repository root): {media}")
        return
    template = load_template()
    result = render(template, media, folder)
    target = media.with_suffix(".tex")
    if target.exists():
        if not force:
            print(f"Exists, skipping: {target.name}")
            return
        existing = target.read_text(encoding="utf-8")
        if existing == result:
            return
        if not any(existing == render(template, sibling, folder) for sibling in siblings):
            print(f"Preserving unrecognized or edited fragment: {target}")
            return
    target.write_text(result, encoding="utf-8")
    print(f"Created: {target}")


def process_file(file_path: str, force: bool = False) -> None:
    media = Path(file_path)
    if not media.is_file():
        print(f"File not found: {file_path}")
    elif parse_filename(media.name)[0] == "UNKNOWN":
        print(f"Skipping (bad format or unsupported extension): {media.name}")
    else:
        process_group(media_groups(media.parent)[media.stem.casefold()], force)


def process_directory(folder: str, force: bool = False) -> None:
    if not os.path.isdir(folder):
        print(f"Folder does not exist: {folder}")
        return
    print(f"\n--- Checking folder: {folder} ---")
    for directory, _, _ in os.walk(folder):
        for siblings in media_groups(Path(directory)).values():
            process_group(siblings, force)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate empty LaTeX solution files for Bagrut question PDFs/images."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional file(s) or directory(ies) to process. Defaults to configured folders.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Refresh existing stubs only if they exactly match the current template for this question.",
    )
    args = parser.parse_args()

    if args.targets:
        for target in args.targets:
            if os.path.isdir(target):
                process_directory(target, force=args.force)
            else:
                print(f"=== Processing single file: {target} ===")
                process_file(target, force=args.force)
    else:
        print("=== No arguments provided. Running batch mode on configured folders... ===")
        for folder in FOLDERS:
            process_directory(folder, force=args.force)

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
