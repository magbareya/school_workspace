"""Generate Bagrut solution stubs from question images or PDFs."""

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
from functools import lru_cache
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(__file__))
from utils import SUPPORTED_EXTENSIONS, parse_filename


@dataclass(frozen=True)
class FolderTemplateConfig:
    template_path: str
    pdf_command_template: str


DEFAULT_PDF_COMMAND = "\\importpdfpage{ {filepath} }{1}"
# \includepdf starts a new page, so the contents entry (\bagrutTocEntry, defined by the
# %PDF lines of the OOP template) is placed on the first imported page.
OOP_PDF_COMMAND = "\\includepdf[pages=-,pagecommand={\\thispagestyle{empty}\\bagrutTocEntry}]{{filepath}}"

IMAGE_COMMAND_TEMPLATE = """\\noindent
\\makebox[\\textwidth][c]{\\includegraphics[width=0.9\\paperwidth,keepaspectratio]{ {filepath} }%
}%"""

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_BASICS = os.path.join(TEMPLATE_DIR, "empty_sol_template_basics.tex")
TEMPLATE_OOP = os.path.join(TEMPLATE_DIR, "empty_sol_template_oop.tex")
TEMPLATE_DEFAULT = os.path.join(TEMPLATE_DIR, "empty_sol_template.tex")

DEFAULT_FOLDER_CONFIG = FolderTemplateConfig(
    template_path=TEMPLATE_DEFAULT,
    pdf_command_template=DEFAULT_PDF_COMMAND,
)

FOLDER_CONFIGS: Dict[str, FolderTemplateConfig] = {
    "basics": FolderTemplateConfig(
        template_path=TEMPLATE_BASICS,
        pdf_command_template=DEFAULT_PDF_COMMAND,
    ),
    "oop": FolderTemplateConfig(
        template_path=TEMPLATE_OOP,
        pdf_command_template=OOP_PDF_COMMAND,
    ),
    "computational_models": DEFAULT_FOLDER_CONFIG,
}

# Default folders processed in batch mode
FOLDERS: List[str] = [
    "bagrut_questions/computational_models",
    "bagrut_questions/basics",
    "bagrut_questions/oop",
]


def build_image_command(folder_name: str, extension: str, latex_relative_path: str) -> str:
    """Return the LaTeX inclusion command for a question PDF or image."""
    config = FOLDER_CONFIGS.get(folder_name, DEFAULT_FOLDER_CONFIG)
    if extension == "pdf":
        return config.pdf_command_template.replace("{filepath}", latex_relative_path)
    return IMAGE_COMMAND_TEMPLATE.replace("{filepath}", latex_relative_path)


@lru_cache(maxsize=None)
def template_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def render(template: str, media: Path, subject: str, folder: str) -> str:
    _, year, model, number, extension = parse_filename(media.name)
    path = f"../../../bagrut_questions/{folder}/{media.name}"
    command = build_image_command(subject, extension, path)
    return (select_variant(template, extension).replace("[[IMAGE_COMMAND]]", command)
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
    subject = folder.split("/")[0]
    config = FOLDER_CONFIGS.get(subject, DEFAULT_FOLDER_CONFIG)
    template = template_text(Path(config.template_path))
    result = render(template, media, subject, folder)
    target = media.with_suffix(".tex")
    if target.exists():
        if not force:
            print(f"Exists, skipping: {target.name}")
            return
        existing = target.read_text(encoding="utf-8")
        if existing == result:
            return
        # Only an exact, unedited render of the current template may be overwritten.
        if not any(existing == render(template, sibling, subject, folder) for sibling in siblings):
            print(f"Preserving (edited, or generated from an older template): {target}")
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
        help="Regenerate only unedited solution templates; preserve partial and completed solutions.",
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
