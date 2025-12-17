#!/usr/bin/env python3
"""
Removes duplicate PDF files in the specified directory by comparing file sizes.

Usage: python scripts/clean.py [directory]

Example: python scripts/clean.py out
"""
import os
import sys

def remove_duplicates(base_dir: str):
    SOLS_SUFFIX = "_sols"
    PRINTABLE_SUFFIX = "_printable"
    suffixes = [SOLS_SUFFIX, PRINTABLE_SUFFIX]
    # import pdb; pdb.set_trace()

    for root, _, files in os.walk(base_dir):
        orig_files = {f for f in files if f.endswith(".pdf") and not any(f.endswith(suffix + ".pdf") for suffix in suffixes)}
        for f in orig_files:
            orig_path = os.path.join(root, f)
            sols_file_path = os.path.join(root, f[: -len(".pdf")] + SOLS_SUFFIX + ".pdf")
            printable_file_path = os.path.join(root, f[: -len(".pdf")] + PRINTABLE_SUFFIX + ".pdf")
            size_orig = os.path.getsize(orig_path)
            try:
                if os.path.isfile(sols_file_path):
                    sols_size = os.path.getsize(sols_file_path)
                    if abs(size_orig - sols_size) <= 200:
                        print(f"Removing duplicate {sols_file_path}")
                        os.remove(sols_file_path)
                if os.path.isfile(printable_file_path):
                    printable_size = os.path.getsize(printable_file_path)
                    if abs(size_orig - printable_size) <= 200:
                        print(f"Removing duplicate {printable_file_path}")
                        os.remove(printable_file_path)
                if os.path.isfile(sols_file_path) and os.path.isfile(printable_file_path):
                    sols_size = os.path.getsize(sols_file_path)
                    printable_size = os.path.getsize(printable_file_path)
                    if abs(sols_size - printable_size) <= 200:
                        print(f"Removing duplicate {sols_file_path}")
                        os.remove(sols_file_path)
            except Exception as e:
                print(f"Error checking duplications of {orig_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "out"
    remove_duplicates(base)
