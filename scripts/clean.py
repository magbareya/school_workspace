#!/usr/bin/env python3
"""
Removes redundant PDF variants (_sols, _printable, _wb, _wb_sols) when rendered
page content is identical.

Usage:
    python scripts/clean.py [directory]

Example:
    python scripts/clean.py out
"""
import argparse
import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

SOLS_SUFFIX = "_sols"
PRINTABLE_SUFFIX = "_printable"
WB_SUFFIX = "_wb"
WB_SOLS_SUFFIX = "_wb_sols"

ALL_VARIANT_SUFFIXES = (WB_SOLS_SUFFIX, SOLS_SUFFIX, PRINTABLE_SUFFIX, WB_SUFFIX)


def are_pdfs_equivalent(path_a: str, path_b: str) -> bool:
    """Compare bytes or rendered pages; uncertainty must never cause deletion."""
    if os.path.getsize(path_a) == os.path.getsize(path_b):
        with open(path_a, "rb") as file_a, open(path_b, "rb") as file_b:
            while True:
                chunk_a = file_a.read(65536)
                chunk_b = file_b.read(65536)
                if chunk_a != chunk_b:
                    break
                if not chunk_a:
                    return True
    if fitz is not None:
        try:
            with fitz.open(path_a) as doc_a, fitz.open(path_b) as doc_b:
                if len(doc_a) != len(doc_b):
                    return False
                for page_a, page_b in zip(doc_a, doc_b):
                    if page_a.rect != page_b.rect:
                        return False
                    if page_a.get_text("text") != page_b.get_text("text"):
                        return False
                    pix_a = page_a.get_pixmap(dpi=150, alpha=False)
                    pix_b = page_b.get_pixmap(dpi=150, alpha=False)
                    if pix_a.samples != pix_b.samples:
                        return False
                return True
        except Exception:
            pass

    return False


def _remove_if_duplicate(reference_path: str, candidate_path: str) -> bool:
    """Remove candidate_path if both files exist and have equivalent PDF content."""
    if not (os.path.isfile(reference_path) and os.path.isfile(candidate_path)):
        return False
    if are_pdfs_equivalent(reference_path, candidate_path):
        print(f"Removing duplicate {candidate_path}")
        os.remove(candidate_path)
        return True
    return False


def remove_duplicates(base_dir: str) -> None:
    if fitz is None:
        print("Warning: PyMuPDF is unavailable; only byte-identical PDFs can be removed.", file=sys.stderr)
    if not os.path.isdir(base_dir):
        return

    for root, _, files in os.walk(base_dir):
        # Landscape pairs are independent targets: compare them even without a regular PDF.
        for wb in sorted(name for name in files if name.endswith(WB_SUFFIX + ".pdf")):
            wb_path = os.path.join(root, wb)
            try:
                _remove_if_duplicate(wb_path, wb_path[: -len(".pdf")] + SOLS_SUFFIX + ".pdf")
            except OSError as e:
                print(f"Error checking duplications of {wb_path}: {e}", file=sys.stderr)
        orig_files = sorted(
            f
            for f in files
            if f.endswith(".pdf")
            and not any(f.endswith(suffix + ".pdf") for suffix in ALL_VARIANT_SUFFIXES)
        )

        for f in orig_files:
            stem = f[: -len(".pdf")]
            orig_path = os.path.join(root, f)
            sols_path = os.path.join(root, f"{stem}{SOLS_SUFFIX}.pdf")
            printable_path = os.path.join(root, f"{stem}{PRINTABLE_SUFFIX}.pdf")

            try:
                _remove_if_duplicate(orig_path, sols_path)
                _remove_if_duplicate(orig_path, printable_path)
                _remove_if_duplicate(printable_path, sols_path)
            except OSError as e:
                print(f"Error checking duplications of {orig_path}: {e}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove duplicate variant PDFs (_sols, _printable, _wb, _wb_sols) in output directory."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default="out",
        help="Target output directory to clean (default: out).",
    )
    args = parser.parse_args()
    remove_duplicates(args.directory)


if __name__ == "__main__":
    main()
