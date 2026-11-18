"""Export code cells from a Jupyter notebook to a C# source file."""

import argparse
import json
import os
import sys
from typing import List

SEPARATOR = "\n\n/* ********************** */\n\n"


def extract_code_cells(notebook_path: str) -> List[str]:
    """Read a .ipynb file and return non-empty code cell contents without magic commands."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    cells: List[str] = []
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue

        raw_source = cell.get("source", [])
        source = "".join(raw_source) if isinstance(raw_source, list) else str(raw_source)
        lines = source.splitlines(keepends=True)

        # Strip leading notebook directives, including .NET Interactive references.
        while lines and (
            not lines[0].strip()
            or lines[0].lstrip().startswith(("#!", "%"))
            or lines[0].lstrip().startswith("#r ")
        ):
            lines.pop(0)
        filtered_lines = lines
        code_text = "".join(filtered_lines).strip()
        if code_text:
            cells.append(code_text)

    return cells


def export_notebook_to_cs(notebook_path: str, output_path: str) -> None:
    if not os.path.isfile(notebook_path):
        print(f"Error: Notebook not found: {notebook_path}", file=sys.stderr)
        sys.exit(1)

    cells = extract_code_cells(notebook_path)
    final_body = SEPARATOR.join(cells)
    if final_body:
        final_body += "\n"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_body)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export C# code cells from a Jupyter notebook to a .cs file."
    )
    parser.add_argument("notebook", help="Path to input .ipynb notebook file.")
    parser.add_argument("outfile", help="Path to output .cs file.")
    args = parser.parse_args()

    export_notebook_to_cs(args.notebook, args.outfile)


if __name__ == "__main__":
    main()
